import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import uuid
from app.config import ENTRIES_FILE, CHUNK_SIZE, CHUNK_OVERLAP
from app.clients.chroma_client import ChromaClient

class DatasetRepository:
    """
    Doc-level registry in entries.json; chunk-level vectors in ChromaDB.
    """
    def __init__(self):
        self._chroma = ChromaClient()
        self._entries: List[Dict] = self._load_entries()

    
    def _load_entries(self) -> List[Dict]:
        if ENTRIES_FILE.exists():
            with open(ENTRIES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_entries(self):
        with open(ENTRIES_FILE, "w", encoding="utf-8") as f:
            json.dump(self._entries, f, ensure_ascii=False, indent=2)

    def list_entries(self) -> List[Dict]:
        return list(self._entries)

    
    def _chunk_text(self, text: str) -> List[str]:
        text = text.strip()
        chunks: List[str] = []
        n = len(text)
        if n == 0:
            return chunks
        start = 0
        size = CHUNK_SIZE
        overlap = CHUNK_OVERLAP
        while start < n:
            end = min(start + size, n)
            chunks.append(text[start:end])
            if end == n:
                break
            start = end - overlap if end - overlap > start else end
        return chunks

    
    def add_pdf_chunks(
        self,
        filename: str,
        full_text_per_page: List[Tuple[int, str]],
        tags: Optional[List[str]] = None,
        language: Optional[str] = None
    ) -> Dict:
        """
        full_text_per_page: [(page_number (1-based), page_text)]
        Returns doc summary + prepared chunk batches (ids, documents, metadatas).
        """
        doc_id = str(uuid.uuid4())
        added_at = datetime.utcnow().isoformat()
        total_chunks = 0

        ids: List[str] = []
        documents: List[str] = []
        metadatas: List[Dict] = []

        for page_num, page_text in full_text_per_page:
            page_text = page_text or ""
            page_chunks = self._chunk_text(page_text)
            for ch in page_chunks:
                chunk_id = f"{doc_id}:{total_chunks}"
                ids.append(chunk_id)
                documents.append(ch)
                metadatas.append({
                    "doc_id": doc_id,
                    "filename": filename,
                    "page": page_num,
                    "chunk_index": total_chunks,
                    "tags": tags or [],
                    "language": language,
                    "added_at": added_at
                })
                total_chunks += 1

        summary = {
            "doc_id": doc_id,
            "filename": filename,
            "pages": len(full_text_per_page),
            "chunks": total_chunks,
            "tags": tags or [],
            "language": language,
            "added_at": added_at
        }

        self._entries.append(summary)
        self._save_entries()

        return {
            "summary": summary,
            "ids": ids,
            "documents": documents,
            "metadatas": metadatas
        }

    
    @property
    def chroma(self) -> ChromaClient:
        return self._chroma

    def get_all_chunks(self):
        return self._chroma.get_all()
