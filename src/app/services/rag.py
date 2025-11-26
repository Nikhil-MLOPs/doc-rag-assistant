from typing import List, Dict, Any

from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama


from langchain.prompts import PromptTemplate

from app.services.vectorstore import get_vector_store


def get_qa_chain():
    """
    Create a RetrievalQA chain:
    - Retrieves chunks from Chroma
    - Sends them to the LLM (Ollama) for answering
    """
    llm = Ollama(
        model="mistral",
        temperature=0.3,
    )

    retriever = get_vector_store().as_retriever(search_kwargs={"k": 4})

    prompt_template = """
You are a helpful assistant. Answer the question based on the provided context.
If the answer is not in the context, say "I don't have enough information."

Question: {question}

Context:
{context}

Answer:
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    return qa_chain


def answer_question(query: str) -> Dict[str, Any]:
    qa_chain = get_qa_chain()
    result = qa_chain.invoke({"query": query})

    answer = result["result"]
    sources = [
        {"text": doc.page_content, "doc_id": doc.metadata.get("doc_id")}
        for doc in result["source_documents"]
    ]
    return {"answer": answer, "sources": sources}
