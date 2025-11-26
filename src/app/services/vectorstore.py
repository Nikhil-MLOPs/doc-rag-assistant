from typing import Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.core.config import settings


_embeddings: Optional[HuggingFaceEmbeddings] = None
_vector_store: Optional[Chroma] = None


def get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        # Small, fast, good-quality sentence embeddings
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings


def get_vector_store() -> Chroma:
    global _vector_store
    if _vector_store is None:
        embeddings = get_embeddings()
        settings.vector_store_dir.mkdir(parents=True, exist_ok=True)
        _vector_store = Chroma(
            collection_name="documents",
            embedding_function=embeddings,
            persist_directory=str(settings.vector_store_dir),
        )
    return _vector_store
