from pathlib import Path

from docling.document_converter import DocumentConverter

from dataweave.adapters.docling import DoclingAdapter


FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "sample_pdf_1.pdf"
)


def get_document():
    converter = DocumentConverter()
    result = converter.convert(FIXTURE_PATH)
    adapter = DoclingAdapter()
    document = adapter.adapt(
        docling_document=result.document,
        document_id="test-doc",
        source=str(FIXTURE_PATH)
    )
    assert document is not None 

    return document

def test_docling_adapter_creates_canonical_document():
    document = get_document()

    document = get_document()

    for i, element in enumerate(document.elements):
        print(
            i,
            element.element_id,
            element.type,
            repr(element.content)
        )

    assert document.document_id == "test-doc"
    assert document.source == str(FIXTURE_PATH)

    assert len(document.elements) > 0
    assert len(document.pages) == 2

"""
def test_docling_adapter_maps_element_fields():
    document = get_document()

    element = document.elements[0]

    assert element.element_id
    assert element.type

    assert element.source is not None
    assert element.source.document_id == "test-doc"
    assert element.source.parser == "docling"
    assert element.source.source_ref == element.element_id
    assert element.source.page is not None

    assert element.bbox is not None
    assert len(element.bbox) == 4


def test_docling_adapter_page_element_ids_are_valid():
    document = get_document()

    element_ids = {
        element.element_id
        for element in document.elements
    }

    for page in document.pages:
        for element_id in page.element_ids:
            assert element_id in element_ids


def test_docling_adapter_preserves_hierarchy():
    document = get_document()

    elements_by_id = {
        element.element_id: element
        for element in document.elements
    }

    for element in document.elements:

        if element.parent_id is not None:
            assert element.parent_id in elements_by_id

        for child_id in element.children_ids:
            assert child_id in elements_by_id

def test_docling_adapter_hierarchy_is_consistent():
    document = get_document()

    elements_by_id = {
        element.element_id: element
        for element in document.elements
    }

    for element in document.elements:

        for child_id in element.children_ids:

            child = elements_by_id[child_id]

            assert child.parent_id == element.element_id

def temp():
    document = get_document()
    for index, ref in enumerate(document):
        print(index, ref.cref)


def test_docling_adapter_page_contains_element_ids():
    document = _get_document()

    all_element_ids = {
        element.element_id
        for element in document.elements
    }

    for page in document.pages:
        assert page.page_number > 0
        assert page.element_ids

        for element_id in page.element_ids:
            assert element_id in all_element_ids


def test_docling_adapter_preserves_expected_content():
    document = _get_document()

    contents = [
        element.content
        for element in document.elements
        if element.content
    ]

    combined_text = "\n".join(contents)

    assert "TECHNICAL ASSESSMENT PAPER" in combined_text
    assert "QA Practical Assessment: Scenario-Based Testing" in combined_text
    assert "INSTRUCTIONS FOR CANDIDATE" in combined_text


def test_docling_adapter_preserves_furniture():
    document = _get_document()

    headers = [
        element
        for element in document.elements
        if element.type == "page_header"
    ]

    footers = [
        element
        for element in document.elements
        if element.type == "page_footer"
    ]

    assert headers
    assert footers

    assert any(
        element.content == "TECHNICAL ASSESSMENT PAPER"
        for element in headers
    )

    assert any(
        element.content == "Page 1 of 2"
        for element in footers
    )

    assert any(
        element.content == "Page 2 of 2"
        for element in footers
    )

"""