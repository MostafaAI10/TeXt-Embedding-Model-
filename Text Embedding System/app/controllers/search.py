from fastapi import APIRouter, HTTPException
from typing import List
from app.models import SearchRequest, SearchHit
from app.services.search_service import semantic_search

router = APIRouter()

@router.post("/search", response_model=List[SearchHit])
def search(payload: SearchRequest):
    try:
        top_k = payload.top_k or 5
        min_sim = payload.min_similarity if payload.min_similarity is not None else 0.4
        tag_filter = payload.tag_filter
        results = semantic_search(payload.query, top_k=top_k, min_similarity=min_sim, tag_filter=tag_filter)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")
