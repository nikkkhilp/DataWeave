from abc import abstractmethod

import pymupdf
from dataweave.core.models     import (CanonicalDocument,
                                       Element,
                                       NormalizedBlock,
                                       NormalizedLine,
                                       TextSpan)
from dataweave.processors.base import DocumentProcessor

class PDFProcessor(DocumentProcessor):

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith(".pdf")

    def process(self, file_path: str) -> CanonicalDocument:
        pdf = pymupdf.open(file_path)   
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
                page       = page_number,
                metadata   = {
                    "total_blocks" : len(blocks)
                },
                source     = {
                    "document_id" : file_path,
                    "page"        : page_number,
                    "parser"      : "pymupdf"
                },
                raw         = {
                    "blocks" : raw_blocks
                }
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