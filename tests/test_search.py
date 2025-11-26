from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_returns_relevant_chunks():
    # 1. Upload a simple document
    file_content = b"Python is great for building machine learning applications."
    upload_resp = client.post(
        "/api/documents",
        files={"file": ("ml_doc.txt", file_content, "text/plain")},
    )
    assert upload_resp.status_code == 201

    # 2. Search for a related query
    search_resp = client.post(
        "/api/search",
        json={"query": "machine learning", "top_k": 3},
    )
    assert search_resp.status_code == 200
    data = search_resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "text" in data[0]
