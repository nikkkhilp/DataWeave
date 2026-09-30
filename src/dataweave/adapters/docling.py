from docling_core.types.doc import DoclingDocument
from dataweave.core.models     import CanonicalDocument, Element, Page, Provenance

class DoclingAdapter:

    def _build_item_lookup(self,
                           docling_document: DoclingDocument):
        items_by_ref = {}
        
        for item in docling_document.texts:
            items_by_ref[item.self_ref] = item

        for item in docling_document.groups:
                    items_by_ref[item.self_ref] = item

        items_by_ref[docling_document.body.self_ref] = docling_document.body

        return items_by_ref

    
    def _walk_items(self, item, items_by_ref):

        yield item

        for child_ref in item.children:
            child = items_by_ref[child_ref.cref]
            yield from self._walk_items(child, items_by_ref)



    # Converts one Docling Text --> one DataWeave element
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
    # Converts one Docling Group --> one DataWeave element
    def _create_group_element(self, item, document_id: str) -> Element:

        source = Provenance(
            document_id = document_id,
            page        = None,
            parser      = "docling",
            source_ref  = item.self_ref
        )
        
        parent_id = None

        if item.parent:
            parent_id = item.parent.cref

        children_ids = [
            child.cref 
            for child in item.children
        ]

        return Element(
            element_id   = item.self_ref,
            type         = item.label.value,
            content      = None,
            parent_id    = parent_id,
            children_ids = children_ids,
            bbox         = None,
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

        pages: dict[int, Page] = {} 

        items_by_ref  = self._build_item_lookup(docling_document) 
        
        ordered_items = self._walk_items(docling_document.body, items_by_ref) 

        body_ids = docling_document.body.self_ref

        text_ids = {
            item.self_ref
            for item in docling_document.texts
        }
        group_ids = {
                    item.self_ref
                    for item in docling_document.groups
                }


        for item in ordered_items : 
            if item.self_ref in text_ids:
                element = self._create_element(
                    item = item,
                    document_id = document_id
                )                          
            elif item.self_ref in group_ids:
                element = self._create_group_element(
                    item = item,
                    document_id = document_id
                )
            elif item.self_ref == body_ids:
                element = self._create_group_element(
                    item = item,
                    document_id = document_id
                )
            else : 
                continue

            document.elements.append(element)
            
            if element.source.page is not None:
                page_number = element.source.page
                
                if page_number not in pages:
                    pages[page_number] = Page(page_number=page_number)

                pages[page_number].element_ids.append(element.element_id)

        document.pages = list(pages.values())
        return document