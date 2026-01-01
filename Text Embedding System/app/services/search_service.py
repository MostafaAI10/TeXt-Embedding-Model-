from typing import Optional, List, Dict
from app.clients.embedder_client import encode
from app.services.entry_service import _get_repo
from app.config import DEFAULT_MIN_SIMILARITY

_repo = _get_repo()

def _to_hits(chroma_query_result) -> List[Dict]:
    hits: List[Dict] = []
    ids = chroma_query_result.get("ids", [[]])[0]
    docs = chroma_query_result.get("documents", [[]])[0]
    metas = chroma_query_result.get("metadatas", [[]])[0]
    dists = chroma_query_result.get("distances", [[]])[0]
    for cid, doc, meta, dist in zip(ids, docs, metas, dists):
        sim = 1.0 - float(dist) if dist is not None else 0.0

        
        tags_str = meta.get("tags")
        tags = tags_str.split(",") if tags_str else None

        hits.append({
            "id": cid,
            "doc_id": meta.get("doc_id"),
            "filename": meta.get("filename"),
            "page": meta.get("page"),
            "chunk_index": meta.get("chunk_index"),
            "text": doc,
            "tags": tags,
            "language": meta.get("language"),
            "added_at": meta.get("added_at"),
            "similarity": sim
        })
    return hits

def semantic_search(query: str, top_k: int = 5, min_similarity: float = DEFAULT_MIN_SIMILARITY, tag_filter: Optional[str] = None):
    q_emb = encode(query)
    result = _repo.chroma.query(query_embeddings=q_emb, top_k=top_k, include=["documents","metadatas","distances","ids"])
    hits = _to_hits(result)

    
    if tag_filter:
        t = tag_filter.lower()
        hits = [h for h in hits if any(t in tag.lower() for tag in (h.get("tags") or []))]

    hits = [h for h in hits if h["similarity"] >= min_similarity]
    hits.sort(key=lambda x: x["similarity"], reverse=True)
    return hits
