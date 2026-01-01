from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PdfUploadResponse(BaseModel):
    doc_id: str
    filename: str
    pages: int
    chunks: int
    tags: Optional[List[str]] = None
    language: Optional[str] = None
    added_at: datetime

class EntryListItem(BaseModel):
    doc_id: str
    filename: str
    pages: int
    chunks: int
    tags: Optional[List[str]] = None
    language: Optional[str] = None
    added_at: datetime
