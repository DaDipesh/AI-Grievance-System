from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    # Local development works out of the box with SQLite.
    # Set DATABASE_URL in backend/.env to use PostgreSQL.
    database_url: str = "sqlite:///./grievance.db"
    jwt_secret: str = "dev-only-change-this-jwt-secret-please"
    jwt_issuer: str = "ai-grievance-system"
    access_token_minutes: int = 30
    upload_dir: str = "./uploads"
    max_upload_bytes: int = 5 * 1024 * 1024
    environment: str = "development"
    admin_registration_id: str = ""
    officer_water_id: str = ""
    officer_electricity_id: str = ""
    officer_street_light_id: str = ""
    officer_road_id: str = ""
    officer_healthcare_id: str = ""
    officer_sanitation_id: str = ""
    officer_drainage_id: str = ""
    officer_environment_id: str = ""

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
