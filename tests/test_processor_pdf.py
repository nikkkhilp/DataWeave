import pymupdf, json, pytest
from pathlib import Path, WindowsPath
from dataweave.processors.pdf_processor import PDFProcessor
from dataweave.core.models import (CanonicalDocument,
                                       Element,
                                       NormalizedBlock,
                                       NormalizedLine,
                                       TextSpan,
                                       LineFeatures,
                                       LineClassification,
                                       ClassifiedLine,
                                       Provenance,
                                       RawEvidence)
from dataweave.core.exceptions import ProcessingError 

"""def test_pdf_processor_extracts_text():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    processor = PDFProcessor()

    document = processor.process(str(pdf_path))

    assert document.source == str(pdf_path)
    assert len(document.elements) > 0
    assert document.elements[0].page == 1



def test_pdf_processor_can_process():
    processor = PDFProcessor()

    assert processor.can_process("report.pdf")
    assert processor.can_process("REPORT.PDF")
    assert not processor.can_process("report.docx")


def test_pdf_dict_output():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    processor = PDFProcessor()
    pdf = pymupdf.open(pdf_path)
    page = pdf[0]
    data = page.get_text("dict")

    print(data)

    pdf.close()


def test_dict_output():
    pdf_path=Path("tests/fixtures/sample_pdf_1.pdf")
    pdf = pymupdf.open(pdf_path)
    page= pdf[0]
    data= page.get_text("dict")

    for block in data["blocks"]:
        print("\nBLOCK : ")
        print("type : ", block.get("type"))
        print("bbox : ", block.get("bbox"))

        for line in block.get("lines", []):
            print(" LINE : ")
            print(" bbox : ", line.get("bbox"))

            for span in line.get("spans", []):
                print("    SPAN:")
                print("    text:", repr(span.get("text")))
                print("    font:", span.get("font"))
                print("    size:", span.get("size"))
                print("    flags:", span.get("flags"))

    pdf.close()


def test_extract_page_spans():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")
    pdf      = pymupdf.open(pdf_path)
    page     = pdf[0]

    processor = PDFProcessor()
    spans     = processor._extract_page_blocks(page)

    pdf.close()

    assert spans
    assert isinstance(spans[0], TextSpan)
    assert spans[0].text
    assert spans[0].font
    assert spans[0].size is not None
    assert spans[0].bbox is not None


def test_extract_page_blocks():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")
    pdf      = pymupdf.open(pdf_path)
    page     = pdf[0]
    processor= PDFProcessor()
    blocks   = processor._extract_page_blocks(page)
    pdf.close()

    assert blocks
    assert isinstance(blocks[0], NormalizedBlock)
    assert isinstance(blocks[0].lines[0], NormalizedLine)
    assert isinstance(blocks[0].lines[0].spans[0], TextSpan)
    assert blocks[0].bbox is not None
    assert blocks[0].lines[0].bbox is not None
    assert blocks[0].lines[0].spans[0].text
    assert blocks[0].lines[0].spans[0].font
    assert blocks[0].lines[0].spans[0].size is not None
    

def test_process():
    pdf_path  = Path("tests/fixtures/sample_pdf_1.pdf")
    processor = PDFProcessor()
    document  = processor.process(pdf_path)

    print(document)


def test_process():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    processor = PDFProcessor()
    document = processor.process(pdf_path)

    assert isinstance(document, CanonicalDocument)
    assert len(document.elements) == 2

    page1 = document.elements[0]

    assert page1.content
    assert page1.raw["blocks"]

    block = page1.raw["blocks"][0]

    assert "block_type" in block
    assert "bbox" in block
    assert block["lines"]

    line = block["lines"][0]

    assert "bbox" in line
    assert line["spans"]

    span = line["spans"][0]

    assert "text" in span
    assert "font" in span
    assert "size" in span
    assert "flags" in span
    assert "bbox" in span


def test_process():
    pdf_path  = Path("tests/fixtures/sample_pdf_1.pdf")
    processor = PDFProcessor()
    document  = processor.process(pdf_path)
    doc_dict  = document.to_dict()

    print(json.dumps(doc_dict, indent=4, default=str))


def test_extract_line_features():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    pdf = pymupdf.open(pdf_path)
    page = pdf[0]

    processor = PDFProcessor()
    blocks = processor._extract_page_blocks(page)

    line = blocks[0].lines[0]

    features = processor._extract_line_features(line)

    pdf.close()

    assert isinstance(features, LineFeatures)
    assert features.text
    assert features.bbox
    assert features.font_sizes
    assert features.fonts
    assert features.text_length > 0


def test_classify_line():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    pdf = pymupdf.open(pdf_path)
    page = pdf[0]

    processor = PDFProcessor()

    blocks = processor._extract_page_blocks(page)

    lines = []

    for block in blocks:
        for line in block.lines:
            features = processor._extract_line_features(line)
            if features.text:
                lines.append(features)

    stats = processor._build_document_stats(lines)

    classification = processor.classify_line(
        lines[0],
        stats,
    )

    pdf.close()

    assert isinstance(classification, LineClassification)
    assert classification.type
    assert 0 <= classification.confidence <= 1
    assert classification.reasons


def test_group_lines():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    pdf = pymupdf.open(pdf_path)
    processor = PDFProcessor()

    page = pdf[0]
    blocks = processor._extract_page_blocks(page)

    lines = []

    for block in blocks:
        for line in block.lines:
            features = processor._extract_line_features(line)

            if features.text:
                lines.append(features)

    stats = processor._build_document_stats(lines)

    classified_lines = [
        ClassifiedLine(
            features=line,
            classification=processor.classify_line(line, stats),
        )
        for line in lines
    ]

    elements = processor._group_lines(
        classified_lines,
        page=1,
    )

    pdf.close()

    for element in elements:
        print("\n---", element.type, "---")
        print(element.content)
        print("confidence:", element.confidence)

    assert elements


def test_add_positional_features():
    lines = [
        LineFeatures(
            text="Heading",
            bbox=(10, 10, 200, 30),
        ),
        LineFeatures(
            text="Paragraph",
            bbox=(10, 50, 300, 70),
        ),
    ]

    processor = PDFProcessor()
    processor._add_positional_features(lines)

    assert lines[0].x_pos == 10
    assert lines[0].y_pos == 10
    assert lines[0].space_after == 20

    assert lines[1].space_before == 20

 

def test_add_indentation_features():
    lines = [
        LineFeatures(
            text="Normal",
            bbox=(10, 10, 100, 30),
        ),
        LineFeatures(
            text="Indented",
            bbox=(30, 40, 120, 60),
        ),
    ]

    processor = PDFProcessor()
    processor._add_indentation_features(lines)

    assert lines[0].indentation == 0
    assert lines[1].indentation == 20




def test_build_line_features():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    pdf = pymupdf.open(pdf_path)

    processor = PDFProcessor()

    blocks = processor._extract_page_blocks(pdf[0])

    normalized_lines = [
        line
        for block in blocks
        for line in block.lines
    ]

    features = processor._build_line_features(normalized_lines)

    pdf.close()

    for feature in features:
        print(
            f"\nTEXT: {feature.text!r}"
            f"\n  font_sizes: {feature.font_sizes}"
            f"\n  bold: {feature.is_bold}"
            f"\n  italic: {feature.is_italic}"
            f"\n  x: {feature.x_pos}"
            f"\n  y: {feature.y_pos}"
            f"\n  before: {feature.space_before}"
            f"\n  after: {feature.space_after}"
            f"\n  indentation: {feature.indentation}"
        )

    assert features
    assert all(feature.text for feature in features)
    assert any(feature.space_before is not None for feature in features)
    assert any(feature.indentation is not None for feature in features)


def test_calculate_horizontal_gaps():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    pdf = pymupdf.open(pdf_path)
    processor = PDFProcessor()
    page = pdf[0]

    words = page.get_text("words")
    print(len(words))


def test_calculate_word_horizontal_gaps():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    pdf = pymupdf.open(pdf_path)
    processor = PDFProcessor()

    gaps = processor._calculate_word_horizontal_gaps(pdf[0])

    print("Number of word gaps:", len(gaps))
    print(
        "Largest word gaps:",
        sorted(gaps, reverse=True)[:20],
    )

    pdf.close()

    assert gaps
    assert all(gap >= 0 for gap in gaps)


def test_build_x_occupancy_profile():
    pdf_path = Path("tests/fixtures/sample_pdf_2.pdf")

    pdf = pymupdf.open(pdf_path)
    processor = PDFProcessor()

    page = pdf[0]

    blocks = processor._extract_page_blocks(page)

    lines = [
        line
        for block in blocks
        for line in block.lines
    ]

    profile = processor._build_x_occupancy_profile(
        lines,
        page_width=page.rect.width,
    )

    assert profile
    assert any(value > 0 for value in profile)

    print("Page width:", page.rect.width)
    print("Bucket count:", len(profile))
    print("Occupancy:", profile)

    pdf.close()


def test_element_can_have_provenance():
    provenance = Provenance(
        document_id="doc1",
        page=2,
        parser="pymupdf",
    )

    element = Element(
        element_id="e1",
        type="paragraph",
        content="Hello world",
        source=provenance,
    )

    assert element.source is provenance
    assert element.source.document_id == "doc1"
    assert element.source.page == 2
    assert element.source.parser == "pymupdf"

def test_element_metadata_and_raw_are_separate():
    raw = RawEvidence(
        parser="pymupdf",
        data={"blocks": []},
    )

    element = Element(
        element_id="e1",
        type="paragraph",
        content="Hello world",
        metadata={"confidence": 0.95},
        raw=raw,
    )

    assert element.metadata["confidence"] == 0.95
    assert element.raw.parser == "pymupdf"
    assert "confidence" not in element.raw.data


def test_process_missing_file_raises_processing_error():
    processor = PDFProcessor()

    with pytest.raises(ProcessingError):
        processor.process("does_not_exist.pdf")


def test_process_invalid_pdf_raises_processing_error(tmp_path):
    invalid_pdf = tmp_path / "invalid.pdf"
    invalid_pdf.write_text("this is not a real PDF")

    processor = PDFProcessor()

    with pytest.raises(ProcessingError):
        processor.process(str(invalid_pdf))



def test_pdf_processor_can_process_only_pdf():
    processor = PDFProcessor()

    assert processor.can_process("document.pdf")
    assert processor.can_process("DOCUMENT.PDF")

    assert not processor.can_process("document.docx")
    assert not processor.can_process("image.png")
"""

def test_pdf_processor_uses_default_config():
    processor = PDFProcessor()

    assert processor.config.strict is False