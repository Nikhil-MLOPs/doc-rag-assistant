# Doc RAG Assistant

Production-style **RAG + LLM document question-answering system**.

## What it does

- Let users upload documents (`.txt`, `.pdf`, `.docx`)
- Chunk and embed documents into a vector store (Chroma)
- Use RAG + LLM (Ollama + LangChain) to answer user questions grounded in the documents
- Provide a simple HTML/CSS frontend
- Use ML engineering best practices:
  - FastAPI backend
  - Docker & Kubernetes manifests
  - DVC for data versioning
  - MLflow for experiment tracking
  - GitHub Actions for CI/CD
  - Prometheus/Grafana for monitoring hooks
  - AWS-friendly deployment story (ECR/EKS style)
