from typing import List

from langchain_core.documents import Document

from app.services.vectorstore import get_vector_store


def retrieve_relevant_chunks(query: str, top_k: int = 4) -> List[Document]:
    vector_store = get_vector_store()
    results: List[Document] = vector_store.similarity_search(query, k=top_k)
    return results
