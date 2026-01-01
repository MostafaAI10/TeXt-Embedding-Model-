# 📄 Semantic Search Engine (FastAPI + Embeddings)

A scalable **Semantic Search Engine** built with **FastAPI** that allows users to upload PDF documents, automatically extract and embed their contents, and perform **semantic + metadata-aware search** across stored documents.

The system follows a clean **CSR (Controller–Service–Repository) architecture**, supports **tag-based filtering**, and is designed to be extensible for multilingual embeddings.

---

## Key Features

- **PDF Upload**
  - Upload PDF files via API
  - Automatic text extraction per page
  - Intelligent chunking for semantic indexing

- **Semantic Search**
  - Vector-based similarity search using embeddings
  - Natural language queries (not keyword-only)

- **Tag Support**
  - Assign multiple tags to PDFs (e.g. `AI, ML, transformers`)
  - Filter search results by tag

- **Multi-Language Ready**
  - Supports multilingual embedding models
  - Language stored as metadata per document

- **Clean Architecture (CSR)**
  - Controller layer (FastAPI routes)
  - Service layer (business logic)
  - Repository layer (data + vector DB)
  - Client layer (embedding models)

---

## 📁 Project Structure

```

text_embedding_system/
├── app
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── controllers
│   │   ├── entries.py
│   │   └── search.py
│   ├── services
│   │   ├── entry_service.py
│   │   └── search_service.py
│   ├── repository
│   │   └── dataset_repo.py
│   └── clients
│       ├── embedder_client.py
│       └── faiss_client.py
└── requirements.txt

```

---

## 🧩 Tech Stack

- **Backend**: FastAPI
- **Language**: Python 3.10+
- **PDF Parsing**: pypdf
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers
- **Validation**: Pydantic
- **Architecture**: CSR Pattern

---

## Author


**Mostafa Abdelhamed**
