import shutil

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)


def setup_module(module):
    # Clean and recreate the raw docs directory for tests
    if settings.raw_docs_dir.exists():
        shutil.rmtree(settings.raw_docs_dir)
    settings.raw_docs_dir.mkdir(parents=True, exist_ok=True)


def test_upload_document():
    file_content = b"Hello, this is a test document."

    response = client.post(
        "/api/documents",
        files={"file": ("test.txt", file_content, "text/plain")},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "test.txt"
    assert data["size_bytes"] == len(file_content)
    assert "id" in data


def test_list_documents():
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0]
    assert "original_filename" in data[0]
