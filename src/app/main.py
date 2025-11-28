from fastapi import FastAPI
import time

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.api.documents import router as documents_router
from app.api.qa import router as qa_router
from app.api.health import router as health_router
from app.core.config import settings
from app.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT


from app.api.health import router as health_router
from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.qa import router as qa_router   # 👈 NEW (just add, don’t replace)
from fastapi.staticfiles import StaticFiles



def create_app() -> FastAPI:
    app = FastAPI(
        title="Doc RAG Assistant API",
        version="0.1.0",
    )

    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            # If an unhandled exception happens, count it as 500
            ERROR_COUNT.labels(request.method, request.url.path).inc()
            raise

        process_time = time.perf_counter() - start_time
        path = request.url.path
        status = response.status_code

        # Optionally skip /metrics itself to avoid noisy self-scrapes
        if path != "/metrics":
            REQUEST_COUNT.labels(request.method, path, status).inc()
            REQUEST_LATENCY.labels(request.method, path).observe(process_time)

            if 500 <= status < 600:
                ERROR_COUNT.labels(request.method, path).inc()

        return response


    # Serve static frontend
    app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

    app.include_router(health_router, prefix="/api")
    app.include_router(documents_router, prefix="/api")
    app.include_router(search_router, prefix="/api")
    app.include_router(qa_router, prefix="/api")   # 👈 NEW (just add)

    @app.get("/", tags=["root"])
    def read_root():
        return {"message": "Doc RAG Assistant backend is running"}

    return app

    @app.get("/metrics")
    def metrics() -> Response:
        """Expose Prometheus metrics for scraping."""
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)




app = create_app()
