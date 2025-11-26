from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", summary="Health check", tags=["health"])
def health_check():
    """
    Simple health check endpoint.

    Returns basic info so we know the app is up and which environment it's running in.
    """
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.environment,
    }
