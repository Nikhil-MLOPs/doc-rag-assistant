from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    top_k: int = Field(4, description="Number of chunks to retrieve", ge=1, le=20)


class RetrievedChunk(BaseModel):
    doc_id: Optional[str] = None
    text: str
    metadata: Dict[str, Any] = {}
