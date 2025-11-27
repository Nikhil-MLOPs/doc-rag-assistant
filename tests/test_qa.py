import socket

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _ollama_available(host: str = "localhost", port: int = 11434, timeout: float = 0.3) -> bool:
    """Return True if an Ollama server is reachable, else False."""
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


@pytest.mark.skipif(
    not _ollama_available(),
    reason="Ollama server not running on localhost:11434",
)
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
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) >= 1
