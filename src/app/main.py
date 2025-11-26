from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.qa import router as qa_router   # 👈 NEW (just add, don’t replace)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Doc RAG Assistant API",
        version="0.1.0",
    )

    app.include_router(health_router, prefix="/api")
    app.include_router(documents_router, prefix="/api")
    app.include_router(search_router, prefix="/api")
    app.include_router(qa_router, prefix="/api")   # 👈 NEW (just add)

    @app.get("/", tags=["root"])
    def read_root():
        return {"message": "Doc RAG Assistant backend is running"}

    return app


app = create_app()
