from abc import abstractmethod
from dataweave.core.exceptions import ProcessingError

import pymupdf
from dataweave.core.models     import (CanonicalDocument,
                                       Element,
                                       NormalizedBlock,
                                       NormalizedLine,
                                       TextSpan,
                                       LineFeatures,
                                       LineClassification,
                                       ClassifiedLine,
                                       SemanticElement,
                                       VisualLineGroup,
                                       Provenance,
                                       RawEvidence)
from dataweave.processors.base import DocumentProcessor
from dataweave.core.config     import ProcessorConfig


class PDFProcessor(DocumentProcessor):

    def __init__(self, config: ProcessorConfig | None=None):
        self.config = config or ProcessorConfig()

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith(".pdf")

    def process(self, file_path: str) -> CanonicalDocument:
        try:
            pdf = pymupdf.open(file_path)   
        except Exception as exc:
            raise ProcessingError(
                f"Falied to open PDf: {file_path}"
            )from exc

        with pdf:
            document = CanonicalDocument(
                document_id = file_path,
                source      = file_path,
            )
            for page_number, page in enumerate(pdf, start=1):

                blocks = self._extract_page_blocks(page)
                raw_blocks   = []
                page_content = []

                for block_index, block in enumerate(blocks, start=1):

                    raw_block = {
                        "block_num"  : block_index,
                        "block_type" : block.block_type,
                        "bbox"       : block.bbox,
                        "lines"      : []
                    }

                    for line_index, line in enumerate(block.lines, start=1):

                        raw_line = {
                            "line_num" : line_index,
                            "bbox"     : line.bbox,
                            "spans"    : []
                        }
                        
                        for span in line.spans:

                            if not span.text:
                                continue
                            page_content.append(span.text)
                            raw_line["spans"].append({
                                "text"  : span.text,
                                "font"  : span.font,
                                "size"  : span.size,
                                "flags" : span.flags,
                                "bbox"  : span.bbox
                            })
                        raw_block["lines"].append(raw_line)
                    raw_blocks.append(raw_block)
                element = Element(
                    element_id = f"{file_path}__page__{page_number}",
                    type       = "raw_text",
                    content    = "\n".join(page_content),
                    metadata   = {
                        "total_blocks" : len(blocks)
                    },
                    source      = Provenance(
                        document_id = file_path,
                        page        = page_number,
                        parser      = "pymupdf"
                    ),
                    raw         = RawEvidence(
                        parser="pymupdf",
                        data   ={
                            "blocks":raw_blocks
                        }
                    )
                )
                document.elements.append(element)
        pdf.close()
        return document



    def _extract_page_blocks(self, page) -> list[NormalizedBlock]:
        data = page.get_text("dict")
        blocks=[]

        for block in data["blocks"]:
            normalized_block = NormalizedBlock(
                block_type   = block["type"],
                bbox         = tuple(block["bbox"]) if block.get("bbox") else None 
            )

            for line in block.get("lines", []):
                normalized_line = NormalizedLine(
                    bbox        = tuple(line["bbox"]) if line.get("bbox") else None
                )                    

                for span in line.get("spans", []):
                    normalized_line.spans.append(
                        TextSpan(
                            text = span["text"],
                            font = span.get("font"),
                            size = span.get("size"),
                            flags= span.get("flags", 0),
                            bbox = tuple(span["bbox"]) if span.get("bbox") else None
                        )
                    )
                normalized_block.lines.append(normalized_line)
            blocks.append(normalized_block)

        return blocks


    def _extract_line_features(self, line: NormalizedLine) -> LineFeatures:
        text_parts =[]
        font_sizes =[]
        fonts      =[]
        flags      =[]

        for span in line.spans:

            text_parts.append(span.text)

            if span.size is not None:
                font_sizes.append(span.size)

            if span.font is not None:
                fonts.append(span.font)

            flags.append(span.flags)
        text = "".join(text_parts).strip()

        return LineFeatures(
            text        = text,
            bbox        = line.bbox,
            font_sizes  = font_sizes,
            fonts       = fonts,
            flags       = flags,
            text_length = len(text),
            is_bold     = any(flag & 16 for flag in flags),
            is_italic   = any(flag & 2  for flag in flags)
        )

    def classify_line(self, features : LineFeatures,
                      document_stats : dict) -> LineClassification:

        text = features.text

        if not text:
            return LineClassification(
                type       = "unknown",
                confidence = 1.0,
                reasons    =["empty_line"]
            )

        reasons = []
        score   = {
            "heading"   : 0.0,
            "paragraph" : 0.0,
            "bullet"    : 0.0,
            "unknown"   : 0.0
        }

        #Bullet detection
        if text.startswith(("•", "-", "–", "—", "*")):
            score["bullet"] += 0.8
            reasons.append("bullet_marker")

        #Short lines are more likely to be headings
        if features.text_length < document_stats["short_line_threshold"]:
            score["heading"] += 0.2
            reasons.append("short_line")

        #Larger font than doc's typical font
        if(
            features.font_sizes
            and 
            max(features.font_sizes) > document_stats["median_font_size"]
        ):
            score["heading"] += 0.4
            reasons.append("learger_than_median")

        #Bold text is a heading singal
        if features.is_bold:
            score["heading"] += 0.3
            reasons.append("bold")

        #If nothing strongly indicates another type, treat it as paragraph.
        if max(score.values()) == 0:
            score["paragraph"] = 0.6
            reasons.append("default_text")

        line_type  = max(score, key=score.get)
        confidence = min(score[line_type], 1.0)

        return LineClassification(
            type       = line_type,
            confidence = confidence,
            reasons    = reasons
        )

    def _build_document_stats(self, lines: list[LineFeatures]) -> dict:

        font_sizes = [
            size
            for line in lines
            for size in line.font_sizes
        ]

        text_lengths = [
            line.text_length
            for line in lines
            if line.text_length > 0
        ]

        if not font_sizes:
            median_font_sizes=0
        else:
            sorted_sizes      = sorted(font_sizes)
            median_font_sizes = sorted_sizes[len(sorted_sizes) // 2]
        if not text_lengths:
            short_line_threshold = 30
        else:
            sorted_lengths = sorted(text_lengths)
            short_line_threshold = sorted_lengths[len(sorted_lengths) // 3]

        return {
            "median_font_size"    : median_font_sizes,
            "short_line_threshold": short_line_threshold
        }

    def _group_lines(self, lines: list[ClassifiedLine], page: int) -> list[SemanticElement]:

        elements=[]
        current = None

        for line in lines:
            classification = line.classification
            line_type      = classification.type

            if line_type == "heading":
                if current is not None:
                    elements.append(current)

                current = SemanticElement(
                    type        = "heading",
                    content     = line.features.text,
                    page        = page,
                    lines       = [line],
                    confidence = classification.confidence 
                )

            elif line_type == "bullet":
                if current is not None:
                    elements.append(current)

                current = SemanticElement(
                    type        = "bullet",
                    content     = line.features.text,
                    page        = page,
                    lines       = [line],
                    confidence = classification.confidence 
                )

            else:
                if current is None:
                    current = SemanticElement(
                    type=line_type,
                    content=line.features.text,
                    page=page,
                    lines=[line],
                    confidence=classification.confidence,
                )
                else:
                    current.lines.append(line)
                    current.content += "\n" + line.features.text
                    current.confidence = min(
                    current.confidence,
                    classification.confidence,
                )

        if current is not None:
            elements.append(current)

        return elements


    def _add_positional_features(self, lines: list[LineFeatures]) -> None:

        for index, line in enumerate(lines):
            if not line.bbox:
                continue

            x0, y0, x1, y1 = line.bbox

            line.x_pos = x0
            line.y_pos = y0

            if index > 0 and lines[index-1].bbox:
                previous_y1 = lines[index-1].bbox[3]
                line.space_before = y0 - previous_y1

            if index < len(lines)-1 and lines[index+1].bbox:
                next_y0 = lines[index+1].bbox[1]
                line.space_after = next_y0 - y1

    def _add_indentation_features(self, lines: list[LineFeatures]) -> None:

        if not lines:
            return

        x_positions = [
            line.bbox[0] for line in lines if line.bbox
        ]

        if not x_positions:
            return

        left_margin = min(x_positions)

        for line in lines:
            if line.bbox:
                line.indentation = line.bbox[0] - left_margin


    def _build_line_features(self, lines: list[NormalizedLine]) -> list[LineFeatures]:

        lines = self._sort_lines_by_reading_order(lines)

        features = [self._extract_line_features(line)
                    for line in lines
                    ]

        self._add_positional_features(features)
        self._add_indentation_features(features)
        return features

    def _sort_lines_by_reading_order(self, lines:list[NormalizedLine]) -> list[NormalizedLine]:
        return sorted(lines, key= lambda line:(
            line.bbox[1], # y position
            line.bbox[0]  # x position
        ))                # We are saying, sort primarily by vertical position, then horizontally.


    def _group_visual_lines(self, lines: list[NormalizedLine]) -> list[VisualLineGroup]:

        if not lines:
            return []

        sorted_lines = self._sort_lines_by_reading_order(lines)
        groups: list[VisualLineGroup] = []

        for line in sorted_lines:
            if not groups:
                groups.append(
                    VisualLineGroup(
                        lines = [line],
                        bbox  = line.bbox
                    )
                )
                continue
            current_group = groups[-1]
            previous_line = current_group.lines[-1]

            if self._same_visual_line(previous_line, line):
                current_group.lines.append(line)
                current_group.bbox = self._merge_bboxes(
                    current_group.bbox,
                    line.bbox
                )
            else:
                groups.append(VisualLineGroup(
                    lines = [line],
                    bbox  = line.bbox
                ))

        return groups

    """
        (x0,y0) ─────────────────── (x1,y0)
            │                           │
            │         TEXT              │
            │                           │
            │                           │
        (x0,y1) ─────────────────── (x1,y1)

        BBOX = (x0, y0, x1, y1)
        
        x0   = left edge
        y0   = top edge
        x1   = right edge
        y1   = bottom edge
    """


    def _same_visual_line(self, first: NormalizedLine, second: NormalizedLine) -> bool:

        first_x0, first_y0, first_x1, first_y1     =  first.bbox
        second_x0, second_y0, second_x1, second_y1 = second.bbox

        first_height  = first_y1  - first_y0
        second_height = second_y1 - second_y0

        if first_height <= 0 or second_height <= 0 :
            return False

        overlap_top      = max(first_y0, second_y0)
        overlap_bottom   = min(first_y1, second_y1)

        overlap        = max(0.0, overlap_bottom - overlap_top)
        smaller_height = min(first_height, second_height)
        overlap_ratio  = overlap/smaller_height

        return overlap_ratio >= 0.5


    def _merge_bboxes(self,
                      first : tuple[float,float,float,float] | None,
                      second: tuple[float,float,float,float] | None
                      )    -> tuple[float,float,float,float] | None:

        if first is None:
            return second
        if second is None:
            return first

        x0 = min(first[0], second[0])
        y0 = min(first[1], second[1])
        x1 = min(first[2], second[2])
        y1 = min(first[3], second[3])

        return (x0, y0, x1, y1)

    def _calculate_horizontal_gaps(self, lines: list[NormalizedLine]) -> list[float]:

        gaps: list[float] = []

        for line in lines:
            spans = sorted(
                line.spans,
                key = lambda span: span.bbox[0]
            )
            for previous, current in zip(spans, spans[1:]):
                gap = current.bbox[0] - previous.bbox[2]
                if gap >= 0:
                    gaps.append(gap)    

        return gaps

    def _calculate_word_horizontal_gaps(self, page) -> list[float]:

        words = page.get_text("words")
        gaps: list[float] = []

        # (block num, line num) -> words on that PDF line
        lines: dict[tuple[int, int], list[tuple]] = {}

        for word in words:

            block_num = word[5]
            line_num  = word[6]
            key = (block_num, line_num)
            lines.setdefault(key, []).append(word)

        for line_words in lines.values():

            line_words.sort(key=lambda word: word[0])

            for previous, current in zip(line_words, line_words[1:]):

                previous_x1 = previous[2]
                current_x1  = current[0]
                gap = current_x1 - previous_x1
                if gap >= 0:
                    gaps.append(gap)

        return gaps

    def _build_x_occupancy_profile(self, lines: list[NormalizedLine],
                                   page_width: float, bucket_size: float = 10.0) -> list[int]:

        if not lines:
            return []

        bucket_count = int(page_width/bucket_size) +1
        occupancy    = [0]*bucket_count 
        # Creates a list occupancy with value 0s and numebr of element same as bucket_count
        
        for line in lines:

            if line.bbox is None:
                continue
            x0, _, x1, _ = line.bbox
            start_bucket = int(x0/bucket_size)
            end_bucket   = int(x1/bucket_size)

            for bucket in range(start_bucket, end_bucket+1):
                if 0 <= bucket < bucket_count:
                    occupancy[bucket] += 1

        return occupancy