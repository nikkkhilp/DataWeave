import json
from docling.document_converter import DocumentConverter

PDF_PATH = "tests/fixtures/sample_pdf_1.pdf"

def main():
    converter = DocumentConverter()
    result    = converter.convert(PDF_PATH)
    document  = result.document

    inspect_body_reference(document)

def inspect_body_reference(docling_document):
    for page_num, page in docling_document.pages.items():
        print(page_num,
              page.size.width,
              page.size.height)


def inspect_body_order(docling_document):
    print("\n=== BODY CHILDREN ORDER ===\n")
    for index, ref in enumerate(docling_document.body.children):
        print(index, ref.cref)
    print("\n=== END ===\n")

def inspect_item(item, index):
    print(f"\n{'n'*60}")
    print(f"ITEN {index}")
    print(f"{'='*60}")

    print("Python type :", type(item))
    print("Item type:", getattr(item, "label", None))

    # Text/content
    for attribute in ["text", "content", "name"]:
        value = getattr(item, attribute, None)
        if value is not None:
            print(f"{attribute}:", value)

    # Provenance
    provenance = getattr(item, "prov", None)
    print("Provenance:", provenance)

    # Parent / children / references
    for attribute in ["parent", "children", "refs"]:
        value = getattr(item, attribute, None)
        if value is not None:
            print(f"{attribute}:", value)


if __name__ == "__main__":
    main()