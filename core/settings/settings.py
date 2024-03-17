from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Example API"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "postgresql+psycopg://test:test@localhost:5432/testtaskbnn"

    project_root: Path = Path(__file__).parent.parent.parent.resolve()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()