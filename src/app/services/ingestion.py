from pathlib import Path
from typing import Dict, List, Optional

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.services.vectorstore import get_vector_store


def _get_loader(file_path: Path):
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(str(file_path))
    if ext == ".docx":
        return Docx2txtLoader(str(file_path))
    if ext == ".txt":
        return TextLoader(str(file_path), encoding="utf-8")

    raise ValueError(f"Unsupported file type for ingestion: {ext}")


def ingest_document(
    doc_id: str, file_path: Path, extra_metadata: Optional[Dict] = None
) -> int:
    """
    Load a document file, split it into chunks, and add them to the vector store.

    Returns the number of chunks added.
    """
    loader = _get_loader(file_path)
    raw_docs: List[Document] = loader.load()

    base_metadata = {"doc_id": doc_id, "source": str(file_path)}
    if extra_metadata:
        base_metadata.update(extra_metadata)

    for d in raw_docs:
        d.metadata.update(base_metadata)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(raw_docs)

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    vector_store.persist()

    return len(chunks)
