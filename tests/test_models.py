import json
from dataweave.core.models import Element, CanonicalDocument

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

"""