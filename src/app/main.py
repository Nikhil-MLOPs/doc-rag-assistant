from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.documents import router as documents_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Doc RAG Assistant API",
        version="0.1.0",
    )

    # Include routers
    app.include_router(health_router, prefix="/api")
    app.include_router(documents_router, prefix="/api")

    @app.get("/", tags=["root"])
    def read_root():
        return {"message": "Doc RAG Assistant backend is running"}

    return app


# Uvicorn will look for this `app` variable
app = create_app()
