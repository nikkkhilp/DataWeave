import pymupdf
from dataweave.core.models     import CanonicalDocument, Element
from dataweave.processors.base import DocumentProcessor

class PDFProcessor(DocumentProcessor):

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith(".pdf")

    def process(self, file_path: str) -> CanonicalDocument:
        pdf = pymupdf.open(file_path)
        for page in pdf:
            print(page.get_text("blocks"))
            
        document = CanonicalDocument(
            document_id = file_path,
            source      = file_path,
        )

        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text().strip()

            if not text:
                continue

            element = Element(
                element_id = f"{file_path}_page_{page_number}",
                type       = "paragraph",
                content    = text,
                page       = page_number,
                source     = {
                    "document_id" : file_path,
                    "page"        : page_number,
                    "parser"      : "pymupdf",
                }
            )
            document.elements.append(element)

        pdf.close()

        return document