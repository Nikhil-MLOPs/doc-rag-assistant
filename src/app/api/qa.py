from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from app.services.rag import answer_question


class QARequest(BaseModel):
    query: str


class QAResponse(BaseModel):
    answer: str
    sources: List[Dict]


router = APIRouter()


@router.post(
    "/qa",
    response_model=QAResponse,
    summary="Ask question using RAG (LLM + retrieval)",
    tags=["qa"],
)
def ask_question(payload: QARequest):
    """
    Full RAG pipeline: retrieve relevant docs, and generate answer using LLM.
    """
    result = answer_question(payload.query)
    return result
