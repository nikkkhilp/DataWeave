import pymupdf
from pathlib import Path
from dataweave.processors.pdf_processor import PDFProcessor

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
"""

def test_pdf_dict_output():
    pdf_path = Path("tests/fixtures/sample_pdf_1.pdf")

    processor = PDFProcessor()
    pdf = pymupdf.open(pdf_path)
    page = pdf[0]
    data = page.get_text("dict")

    print(data)

    pdf.close()