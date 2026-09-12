<img width="1933" height="814" alt="dataweave_logo" src="https://github.com/user-attachments/assets/04c465ca-806f-4311-a5f9-138bbb335488" />


                    ┌──────────────────────┐
                    │      Input File      │
                    └──────────┬───────────┘
                               ↓
                     File Type Detection
                               ↓
              ┌────────────────────────────────┐
              │        Format Processor        │
              │ PDF / DOCX / PPTX / XLSX / ...│
              └────────────────┬───────────────┘
                               ↓
                  Raw Extraction + Layout
                               ↓
              ┌────────────────────────────────┐
              │      Canonical Evidence        │
              │ text + bbox + font + images +  │
              │ tables + page + provenance     │
              └────────────────┬───────────────┘
                               ↓
                    Document Understanding
                               ↓
        ┌──────────────────────┴──────────────────────┐
        ↓                                             ↓
Deterministic / statistical                    AI / VLM fallback
analysis                                       for ambiguity
        ↓                                             ↓
        └──────────────────────┬──────────────────────┘
                               ↓
                    Structure Reconstruction
                               ↓
                      Canonical Document
                               ↓
                     Chunking-ready output
