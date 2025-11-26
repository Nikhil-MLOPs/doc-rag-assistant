from typing import List

from fastapi import APIRouter

from app.models.query import RetrievedChunk, SearchRequest
from app.services.retrieval import retrieve_relevant_chunks

router = APIRouter()


@router.post(
    "/search",
    response_model=List[RetrievedChunk],
    summary="Search indexed documents and return relevant chunks",
    tags=["search"],
)
def search_documents(payload: SearchRequest):
    """
    Search across all ingested documents and return the most relevant chunks.

    This is the retrieval-only part of RAG (no LLM yet).
    """
    docs = retrieve_relevant_chunks(payload.query, payload.top_k)

    results: List[RetrievedChunk] = []

    for d in docs:
        results.append(
            RetrievedChunk(
                doc_id=d.metadata.get("doc_id"),
                text=d.page_content,
                metadata=d.metadata or {},
            )
        )

    return results
