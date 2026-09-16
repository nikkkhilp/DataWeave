<img width="1933" height="814" alt="dataweave_logo" src="https://github.com/user-attachments/assets/04c465ca-806f-4311-a5f9-138bbb335488" />

                         DATAWEAVE
                             │
                     ┌───────▼────────┐
                     │ Format Router  │
                     └───────┬────────┘
                             │
               ┌─────────────┼─────────────┐
               │             │             │
              PDF           DOCX          XLSX
               │
               ▼
        ┌───────────────┐
        │ Native layer  │
        │ PyMuPDF       │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Primary       │
        │ Docling       │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Quality       │
        │ Engine        │
        └───────┬───────┘
                │
          ┌─────┴─────┐
          │           │
        GOOD        BAD/UNCERTAIN
          │           │
          │      ┌────┴─────┐
          │      │          │
          │   MinerU      Marker
          │      │          │
          │      └────┬─────┘
          │           │
          │      still bad?
          │           │
          │           ▼
          │          VLM
          │           │
          └─────┬─────┘
                ▼
       ┌───────────────────┐
       │ DataWeave         │
       │ Canonical IR      │
       └─────────┬─────────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
       RAG     Agents   Other apps