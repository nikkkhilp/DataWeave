import pymupdf, json
from pathlib import Path, WindowsPath
from dataweave.processors.pdf_processor import PDFProcessor
from dataweave.core.models import (CanonicalDocument,
                                       Element,
                                       NormalizedBlock,
                                       NormalizedLine,
                                       TextSpan)

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

"""
def test_process():
    pdf_path  = Path("tests/fixtures/sample_pdf_1.pdf")
    processor = PDFProcessor()
    document  = processor.process(pdf_path)
    doc_dict  = document.to_dict()

    print(json.dumps(doc_dict, indent=4, default=str))