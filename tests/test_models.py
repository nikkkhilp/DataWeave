import json
from dataweave.core.models import Element, CanonicalDocument, Provenance

"""
def test_document_to_dict():
    document = CanonicalDocument(
        document_id = "doc_001",
        source = "annual_report.pdf",
    )

    document.elements.append(
        Element(
            element_id = "el_001",
            type = "heading",
            content = "Annual Revenue",
            page = 4,
        )
    )

    data = document.to_dict()

    assert data["document_id"] == "doc_001"
    assert data["source"] == "annual_report.pdf"
    assert len(data["elements"]) == 1
    assert data["elements"][0]["type"] == "heading"


def test_document_to_json():
    document  = CanonicalDocument(
        document_id = "doc_001",
        source = "annual_report.pdf",
    )

    document.elements.append(
        Element(
            element_id = "el_001",
            type = "heading",
            content = "Annual Revenue",
            page = 4,
        )
    )

    data = document.to_dict()
    json_data = json.dumps(data)

    assert isinstance(json_data, str)

def test_element_provenance():
    element = Element(
        element_id = "el_001",
        type = "paragraph",
        content = "Revenue increased by 24%.",
        page = 4,
        source = {
            "document_id" : "doc_001",
            "page" : 4
        }
    )

    assert element.source["document_id"] == "doc_001"
    assert element.source["page"] == 4


def test_canonical_document_can_contain_elements():
    element = Element(
        element_id="e1",
        type="paragraph",
        content="Hello world",
        page=1,
    )

    document = CanonicalDocument(
        document_id="doc1",
        source="test.pdf",
        elements=[element],
    )

    assert document.document_id == "doc1"
    assert document.source == "test.pdf"
    assert len(document.elements) == 1
    assert document.elements[0].content == "Hello world"

    

def test_canonical_document_to_dict():
    element = Element(
        element_id="e1",
        type="paragraph",
        content="Hello world",
        page=1,
    )

    document = CanonicalDocument(
        document_id="doc1",
        source="test.pdf",
        elements=[element],
    )

    result = document.to_dict()

    assert result["document_id"] == "doc1"
    assert result["elements"][0]["content"] == "Hello world"



def test_provenance():
    provenance = Provenance(
        document_id="doc1",
        page=2,
        parser="pymupdf",
    )

    assert provenance.document_id == "doc1"
    assert provenance.page == 2
    assert provenance.parser == "pymupdf"


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
        metadata={"metadata":"doc1"},
        raw={"raw":"raw"},
        source=provenance,
    )

    assert element.source is provenance
    assert element.source.document_id == "doc1"
    assert element.source.page == 2
    assert element.source.parser == "pymupdf"

"""
