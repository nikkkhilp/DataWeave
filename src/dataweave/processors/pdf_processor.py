import pymupdf
from dataweave.core.models     import CanonicalDocument, Element, TextSpan
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
            spans = self._extract_page_spans(page)

            for index, span in enumerate(spans):
                if not span.text.strip():
                    continue

                element = Element(
                    element_id = f"{file_path}_page_{page_number}_span_{index}",
                    type       = "raw_text",
                    content    = span.text,
                    page       = page_number,
                    metadata   = {
                        "font" : span.font,
                        "szie" : span.size,
                        "flags": span.flags,
                        "bbox" : span.bbox
                    },
                    source     = {
                        "document_id" : file_path,
                        "page"        : page_number,
                        "parser"      : "pymupdf",
                    }
                )
            document.elements.append(element)

        pdf.close()
        return document

    def _extract_page_spans(self, page) -> list[TextSpan]:
        data = page.get_text("dict")
        spans=[]

        for block in data["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    spans.append(
                        TextSpan(
                            text = span["text"],
                            font = span.get("font"),
                            size = span.get("size"),
                            flags= span.get("flags", 0),
                            bbox = tuple(span["bbox"]) if span.get("bbox") else None
                        )
                    )
        return spans