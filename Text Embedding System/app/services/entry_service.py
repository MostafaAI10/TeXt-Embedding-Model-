from typing import List, Tuple, Optional
import io
from pypdf import PdfReader
from fastapi import HTTPException
from datetime import datetime

from app.clients.embedder_client import encode
from app.repository.dataset_repo import DatasetRepository

_repo = DatasetRepository()

def _extract_pdf_pages(file_bytes: bytes) -> List[Tuple[int, str]]:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {e}")

    pages: List[Tuple[int, str]] = []
    for i, page in enumerate(reader.pages):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        pages.append((i + 1, txt))
    return pages

def upload_pdf(file_bytes: bytes, filename: str, tags: Optional[List[str]] = None, language: Optional[str] = None):
    
    page_texts = _extract_pdf_pages(file_bytes)

    if not any((t or "").strip() for _, t in page_texts):
        raise HTTPException(status_code=400, detail="No extractable text found in the uploaded PDF.")

    
    tags_str = ",".join(tags) if tags else None

    
    prepared = _repo.add_pdf_chunks(
        filename=filename,
        full_text_per_page=page_texts,
        tags=tags_str,        
        language=language
    )

    ids = prepared["ids"]
    documents = prepared["documents"]
    metadatas = prepared["metadatas"]

    if len(documents) == 0:
        raise HTTPException(status_code=400, detail="PDF contained no text chunks after processing.")

    
    embeddings = encode(documents)
    _repo.chroma.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

    return prepared["summary"]

def list_entries():
    return _repo.list_entries()

def _get_repo():
    return _repo
