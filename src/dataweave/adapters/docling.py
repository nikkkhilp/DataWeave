from docling_core.types.doc import DoclingDocument
from dataweave.core.models     import CanonicalDocument, Element, Page, Provenance

class DoclingAdapter:

    # Converts one Docling item --> one DataWeave element
    def _create_element(self,
                        item,
                        document_id: str) -> Element:

        source = Provenance(
            document_id = document_id,
            page        = None,
            parser      = "docling",
            source_ref  = item.self_ref
        ) 

        bbox = None

        if item.prov:
            provenance  = item.prov[0]
            source.page = provenance.page_no

            if provenance.bbox:
                bbox = (
                    provenance.bbox.l,
                    provenance.bbox.t,
                    provenance.bbox.r,
                    provenance.bbox.b
                )
        parent_id = None
        if item.parent:
            parent_id = item.parent.cref

        children_ids = [child.cref for child in item.children]
        content      = getattr(item, "text", None)
        element_type = item.label.value

        return Element(
            element_id   = item.self_ref,
            type         = element_type,
            content      = content,
            parent_id    = parent_id,
            children_ids = children_ids,
            bbox         = bbox,
            source       = source
        )



    def adapt(self,
              docling_document: DoclingDocument,
              document_id: str,
              source: str) -> CanonicalDocument:

        document = CanonicalDocument(
            document_id = document_id,
            source      = source
        )

        pages: dict[int, Page] ={} 

        for item, level in docling_document.iterate_items():
            element = self._create_element(
                item = item,
                document_id = document_id)

            document.elements.append(element)

            if element.source and element.source.page is not None:

                page_number = element.source.page

                if page_number not in pages:
                    pages[page_number] = Page(page_number = page_number)

                pages[page_number].element_ids.append(
                    element.element_id
                )   

        document.pages = list(pages.values())

        return document