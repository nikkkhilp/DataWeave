import json
from docling.document_converter import DocumentConverter

PDF_PATH = "tests/fixtures/sample_pdf_1.pdf"

def main():
    converter = DocumentConverter()
    result    = converter.convert(PDF_PATH)
    document  = result.document

    print("DOCUMENT TYPE : ")
    print(type(document))

    print("\nDOCUMENT ATTRIBUTES : ")
    print([name for name in dir(document) if not name.startswith("_")])

    print("\nDOCUMENT ITEMS : ")
    for index, item_data in enumerate(document.iterate_items()):
        print(f"\n{'=' * 60}")
        print(f"ITEM {index}")
        print("Tuple length:", len(item_data))
        print("Tuple:", item_data)

        if index >= 9:
            break

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