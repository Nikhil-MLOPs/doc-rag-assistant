from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_qa_pipeline():
    # Upload a test file
    file_content = b"Python is a popular language for machine learning and AI."
    upload_resp = client.post(
        "/api/documents",
        files={"file": ("ai.txt", file_content, "text/plain")},
    )
    assert upload_resp.status_code == 201

    # Ask a question
    resp = client.post("/api/qa", json={"query": "What is Python used for?"})
    assert resp.status_code == 200

    data = resp.json()
    assert "answer" in data
    assert len(data["sources"]) >= 1
