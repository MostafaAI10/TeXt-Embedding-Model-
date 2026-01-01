import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import numpy as np
from app.config import PERSIST_DIR, CHROMA_COLLECTION

class ChromaClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(PERSIST_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"}  
        )

    def add(
        self,
        ids: List[str],
        documents: List[str],
        metadatas: List[Dict],
        embeddings: Optional[np.ndarray] = None
    ):
        payload = {"ids": ids, "documents": documents, "metadatas": metadatas}
        if embeddings is not None:
            payload["embeddings"] = embeddings.tolist()
        self.collection.add(**payload)

    def query(
        self,
        query_embeddings: np.ndarray,
        top_k: int = 5,
        where: Optional[Dict] = None,
        include: Optional[List[str]] = None
    ):
        include = include or ["documents", "metadatas", "distances", "ids"]
        
        if query_embeddings.ndim == 1:
            q = [query_embeddings.tolist()]
        else:
            q = query_embeddings.tolist()
        return self.collection.query(
            query_embeddings=q,
            n_results=top_k,
            where=where,
            include=include
        )

    def get_all(self):
        return self.collection.get(include=["documents", "metadatas", "ids"])
