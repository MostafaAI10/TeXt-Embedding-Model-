from pydantic import BaseModel

class PdfMeta(BaseModel):
    filename: str
    content_type: str
    size: int
