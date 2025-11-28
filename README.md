📄 Doc-RAG-Assistant

AI-Powered Document Q&A System | FastAPI 🚀 LangChain 🤖 ChromaDB 📚 MLflow 📊 Docker 🐳 AWS EC2 ☁️

🌟 Project Overview

Doc-RAG-Assistant is a production-ready Document Retrieval-Augmented Generation (RAG) system.

It allows users to upload PDFs or text files, extracts content, splits it into chunks, stores it in a vector database, and enables users to ask questions with accurate, context-based answers.

Built using FastAPI, LangChain, HuggingFace Embeddings, ChromaDB, Ollama LLM, MLflow, Docker, and deployed on AWS EC2.

🚀 Key Features

✔ Upload files (PDF, TXT) via Web UI

✔ RAG-based intelligent question answering

✔ Embedding and vector search using ChromaDB

✔ Uses Mistral LLM (via Ollama) for context-based answers

✔ MLflow-based logging (latency, answer stats, sources)

✔ Dockerized and deployed on AWS EC2

✔ CI/CD ready with GitHub Actions

✔ Future support for Kubernetes, Prometheus & Grafana

🧠 System Architecture

Frontend (HTML/JS) → FastAPI Backend → Document Processing → ChromaDB → Ollama LLM → MLflow Logging

🧠 Technologies Used

Layer	Technology

Backend	FastAPI

RAG Engine	LangChain

Embeddings	HuggingFace

Vector DB	ChromaDB

LLM	Ollama (Mistral)

Monitoring	MLflow

Frontend	HTML, Vanilla JS

Testing	Pytest

Deployment	Docker + AWS EC2

CI/CD	GitHub Actions

📦 Project Structure

doc-rag-assistant/
│
├── src/app/

│ ├── api/ (API Routes)

│ │ ├── documents.py

│ │ └── qa.py

│ ├── services/ (Core Business Logic)

│ │ ├── ingestion.py

│ │ ├── vectorstore.py

│ │ └── rag.py

│ ├── frontend/ (Web UI)

│ │ ├── index.html

│ │ ├── app.js

│ │ └── styles.css

│ └── main.py (FastAPI root)

│
├── tests/ (Pytest)

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── README.md

└── .github/workflows/ci.yml

🛠️ Local Setup

1️⃣ Create & activate virtual environment

python -m venv .venv

source .venv/bin/activate (Linux/Mac)

.venv\Scripts\activate (Windows)

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Start FastAPI

uvicorn app.main:app --reload --app-dir src

Access the app:

Frontend → http://127.0.0.1:8000/frontend/

Docs → http://127.0.0.1:8000/docs

🐳 Docker Deployment

Build and run locally:

docker compose up --build

☁️ AWS EC2 Deployment (Dockerized)

On EC2 instance:

sudo apt update && sudo apt install docker.io -y

sudo systemctl enable docker

docker compose up --build -d

Then access:

http://<EC2-PUBLIC-IP>:8000/frontend/

📊 MLflow Logging

Logged automatically:

✔ Answer Latency

✔ Number of Sources

✔ Answer Quality

✔ Query Length

Runs stored in: mlruns folder

🧪 Testing

Run unit tests:

pytest -v

🤖 CI/CD Workflow (GitHub Actions)

Included workflow (.github/workflows/ci.yml) runs:

✔ Install dependencies

✔ Run pytest

✔ Build Docker image

Triggers: push, pull_request

📡 Future Enhancements

🔹 Kubernetes deployment (EKS/Minikube)

🔹 Prometheus Metrics & Grafana Dashboard

🔹 Multi-tenant document support

🔹 Authentication / JWT
