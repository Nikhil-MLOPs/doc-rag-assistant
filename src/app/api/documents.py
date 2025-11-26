from typing import List
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.models.document import DocumentInfo
from app.services.storage import list_documents, save_upload_file
from app.services.ingestion import ingest_document

router = APIRouter()


@router.post(
    "/documents",
    response_model=DocumentInfo,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
    tags=["documents"],
)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document file (.txt, .pdf, .docx).

    The file is stored on disk and indexed into the vector store.
    """
    try:
        doc_info = await save_upload_file(file)

        # Build path to stored file: <doc_id>__<original_filename>
        stored_filename = f"{doc_info.id}__{doc_info.original_filename}"
        file_path = settings.raw_docs_dir / stored_filename

        # Ingest into vector store
        ingest_document(doc_info.id, Path(file_path))

        return doc_info
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get(
    "/documents",
    response_model=List[DocumentInfo],
    summary="List uploaded documents",
    tags=["documents"],
)
def get_documents():
    """
    List all uploaded documents.

    Returns metadata for each stored document.
    """
    return list_documents()
