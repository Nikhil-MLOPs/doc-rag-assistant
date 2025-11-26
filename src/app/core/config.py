from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Doc RAG Assistant"
    environment: str = "local"
    debug: bool = True

    # Base directory (project root) – assuming we run from repo root
    base_dir: Path = Path.cwd()

    # Data directories
    data_dir: Path = base_dir / "data"
    raw_docs_dir: Path = data_dir / "raw"

    class Config:
        env_file = ".env"


settings = Settings()
