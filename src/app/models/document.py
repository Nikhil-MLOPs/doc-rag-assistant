from typing import Optional

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    id: str
    original_filename: str
    size_bytes: int
    content_type: Optional[str] = None
