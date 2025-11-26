import shutil
from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.models.document import DocumentInfo


ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def ensure_data_dirs() -> None:
    settings.raw_docs_dir.mkdir(parents=True, exist_ok=True)


def _sanitize_filename(filename: str) -> str:
    # Basic sanitization: keep only the name part, replace spaces
    name = Path(filename).name
    return name.replace(" ", "_")


async def save_upload_file(file: UploadFile) -> DocumentInfo:
    ensure_data_dirs()

    if not file.filename:
        raise ValueError("File must have a name")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Allowed: .txt, .pdf, .docx")

    doc_id = uuid4().hex
    safe_name = _sanitize_filename(file.filename)
    stored_filename = f"{doc_id}__{safe_name}"
    dest_path = settings.raw_docs_dir / stored_filename

    # Read and save file contents
    with dest_path.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)

    size_bytes = dest_path.stat().st_size

    return DocumentInfo(
        id=doc_id,
        original_filename=safe_name,
        size_bytes=size_bytes,
        content_type=file.content_type,
    )


def list_documents() -> List[DocumentInfo]:
    ensure_data_dirs()

    documents: List[DocumentInfo] = []

    for path in settings.raw_docs_dir.iterdir():
        if not path.is_file():
            continue

        # Expect filenames like: "<id>__<original_name>"
        try:
            doc_id, original_name = path.name.split("__", 1)
        except ValueError:
            # Skip files that don't match our pattern
            continue

        size_bytes = path.stat().st_size

        documents.append(
            DocumentInfo(
                id=doc_id,
                original_filename=original_name,
                size_bytes=size_bytes,
                content_type=None,  # We don't store it yet for listed docs
            )
        )

    return documents
