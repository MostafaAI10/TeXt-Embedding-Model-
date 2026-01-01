from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from datetime import datetime
import logging

from app.models import PdfUploadResponse, EntryListItem 
from app.services.entry_service import upload_pdf, list_entries

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/entries/upload_pdf", response_model=PdfUploadResponse)
async def upload_pdf_entry(
    file: UploadFile = File(...),
    tags: Optional[str] = Form(None),   
    language: Optional[str] = Form(None)
):
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail=f"Unsupported content-type: {file.content_type}. Please upload a PDF.")

    try:
        raw = await file.read()
        tag_list: Optional[List[str]] = None
        if tags:
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]

        summary = upload_pdf(raw, filename=file.filename, tags=tag_list, language=language)

        return PdfUploadResponse(
            doc_id=summary["doc_id"],
            filename=summary["filename"],
            pages=summary["pages"],
            chunks=summary["chunks"],
            tags=summary.get("tags").split(",") if summary.get("tags") else None,
            language=summary.get("language"),
            added_at=datetime.fromisoformat(summary["added_at"])
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

@router.get("/entries", response_model=List[EntryListItem])
def get_entries():
    items = []
    for e in list_entries():
        items.append(EntryListItem(
            doc_id=e["doc_id"],
            filename=e["filename"],
            pages=e["pages"],
            chunks=e["chunks"],
            tags=e.get("tags").split(",") if e.get("tags") else None,
            language=e.get("language"),
            added_at=datetime.fromisoformat(e["added_at"])
        ))
    return items
