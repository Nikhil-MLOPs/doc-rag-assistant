from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.document import DocumentInfo
from app.services.storage import list_documents, save_upload_file

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

    Returns basic information about the stored document.
    """
    try:
        doc_info = await save_upload_file(file)
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
