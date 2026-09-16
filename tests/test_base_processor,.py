import pytest

from dataweave.processors.base import DocumentProcessor
from dataweave.core.models import CanonicalDocument

"""
def test_document_processor_cannot_be_instantiated():
    with pytest.raises(TypeError):
        DocumentProcessor()


def test_concrete_processor_can_be_instantiated():
    class TestProcessor(DocumentProcessor):

        def can_process(self, file_path: str) -> bool:
            return True

        def process(self, file_path: str) -> CanonicalDocument:
            return CanonicalDocument()

    processor = TestProcessor()

    assert processor.can_process("test.pdf") is True


def test_incomplete_processor_cannot_be_instantiated():
    class IncompleteProcessor(DocumentProcessor):

        def can_process(self, file_path: str) -> bool:
            return True

    with pytest.raises(TypeError):
        IncompleteProcessor()
"""