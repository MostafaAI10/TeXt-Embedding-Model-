from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    min_similarity: Optional[float] = 0.4
    tag_filter: Optional[str] = None

class SearchHit(BaseModel):
    id: str                 
    doc_id: str
    filename: str
    page: Optional[int] = None
    chunk_index: int
    text: str
    tags: Optional[List[str]] = None
    language: Optional[str] = None
    added_at: datetime
    similarity: float
