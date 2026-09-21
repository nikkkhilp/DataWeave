from pathlib import Path
from docling.document_converter import DocumentConverter
from dataweave.adapters.docling import DoclingAdapter


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_pdf_1.pdf"

"""
def test_docling_adapter_creates_canonical_document():
    converter = DocumentConverter()

    result = converter.convert(FIXTURE_PATH)
    docling_document = result.document

    adapter = DoclingAdapter()

    document = adapter.adapt(
        docling_document=docling_document,
        document_id="test-doc",
        source=str(FIXTURE_PATH),
    )

    # Basic document structure
    assert document.document_id == "test-doc"
    assert document.source == str(FIXTURE_PATH)

    # We should have extracted elements
    assert len(document.elements) > 0

    # Our sample PDF has two pages
    assert len(document.pages) == 2


def test_docling_adapter_maps_element_fields():
    converter = DocumentConverter()

    result = converter.convert(FIXTURE_PATH)
    docling_document = result.document

    adapter = DoclingAdapter()

    document = adapter.adapt(
        docling_document=docling_document,
        document_id="test-doc",
        source=str(FIXTURE_PATH),
    )

    element = document.elements[0]

    # Element identity
    assert element.element_id
    assert element.type

    # Source information
    assert element.source is not None
    assert element.source.document_id == "test-doc"
    assert element.source.parser == "docling"
    assert element.source.source_ref == element.element_id

    # Page provenance
    assert element.source.page is not None

    # Bounding box
    assert element.bbox is not None
    assert len(element.bbox) == 4


def test_docling_adapter_preserves_hierarchy():
    converter = DocumentConverter()

    result = converter.convert(FIXTURE_PATH)
    docling_document = result.document

    adapter = DoclingAdapter()

    document = adapter.adapt(
        docling_document=docling_document,
        document_id="test-doc",
        source=str(FIXTURE_PATH),
    )

    # At least one element should have a parent.
    child_elements = [
        element
        for element in document.elements
        if element.parent_id is not None
    ]

    assert child_elements

    # At least one element should have children.
    parent_elements = [
        element
        for element in document.elements
        if element.children_ids
    ]

    assert parent_elements


def test_docling_adapter_page_contains_element_ids():
    converter = DocumentConverter()

    result = converter.convert(FIXTURE_PATH)
    docling_document = result.document

    adapter = DoclingAdapter()

    document = adapter.adapt(
        docling_document=docling_document,
        document_id="test-doc",
        source=str(FIXTURE_PATH),
    )

    all_element_ids = {
        element.element_id
        for element in document.elements
    }

    for page in document.pages:
        assert page.page_number > 0
        assert page.element_ids

        for element_id in page.element_ids:
            assert element_id in all_element_ids
"""

def test_docling_adapter_preserves_expected_content():
    converter = DocumentConverter()

    result = converter.convert(FIXTURE_PATH)
    docling_document = result.document

    adapter = DoclingAdapter()

    document = adapter.adapt(
        docling_document=docling_document,
        document_id="test-doc",
        source=str(FIXTURE_PATH),
    )

    contents = [
        element.content
        for element in document.elements
        if element.content
    ]

    combined_text = "\n".join(contents)

    assert "TECHNICAL ASSESSMENT PAPER" in combined_text
    assert "QA Practical Assessment: Scenario-Based Testing" in combined_text
    assert "INSTRUCTIONS FOR CANDIDATE" in combined_text
