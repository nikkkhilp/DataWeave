from dataweave.core.models import  CanonicalDocument, Element
from dataweave.processors.base import DocumentProcessor

class FakeProcessor(DocumentProcessor):
    def can_process(self, file_path:str) -> bool:
        return file_path.endswith(".fake")

    def process(self, file_path:str) -> CanonicalDocument:
        document = CanonicalDocument(
            document_id="doc_001",
            source     =file_path
        )

        document.elements.append(
            Element(
                element_id="el_001",
                type="paragraph",
                content="This is a fake document.",
                page=1
            )
        )

        return document