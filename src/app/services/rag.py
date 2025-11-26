from typing import Dict, Any
import time

from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

from app.services.vectorstore import get_vector_store

import mlflow


MLFLOW_EXPERIMENT_NAME = "doc-rag-assistant-qa"


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

    # This should match what you're using in retrieval
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
        input_variables=["context", "question"],
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
    """
    Run the full RAG pipeline and log the run in MLflow.
    """
    # Configure MLflow to use local directory "mlruns"
    mlflow.set_tracking_uri("file:mlruns")
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    qa_chain = get_qa_chain()

    start_time = time.time()

    with mlflow.start_run(run_name="online_qa"):
        # Log parameters (things that describe the setup)
        mlflow.log_param("llm_model", "mistral")
        mlflow.log_param("retriever_top_k", 4)
        mlflow.log_param("chunk_size", 1000)
        mlflow.log_param("chunk_overlap", 200)

        # Input
        mlflow.log_param("query", query[:200])  # truncate long queries

        # Run the chain
        result = qa_chain.invoke({"query": query})

        answer: str = result["result"]
        source_docs = result.get("source_documents", [])

        latency = time.time() - start_time

        # Metrics
        mlflow.log_metric("latency_sec", latency)
        mlflow.log_metric("answer_length", len(answer))
        mlflow.log_metric("num_sources", len(source_docs))

        # You could also log some example output as text:
        mlflow.log_text(answer, artifact_file="answer.txt")

        sources = [
            {"text": doc.page_content, "doc_id": doc.metadata.get("doc_id")}
            for doc in source_docs
        ]

    return {"answer": answer, "sources": sources}
