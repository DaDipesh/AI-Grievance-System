from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    # Local development works out of the box with SQLite.
    # Set DATABASE_URL in backend/.env to use PostgreSQL.
    # Keep the development database anchored to this backend directory even
    # when Uvicorn is started from the repository root or an IDE terminal.
    database_url: str = f"sqlite:///{(BASE_DIR / 'grievance.db').as_posix()}"
    jwt_secret: str = "dev-only-change-this-jwt-secret-please"
    jwt_issuer: str = "ai-grievance-system"
    access_token_minutes: int = 30
    upload_dir: str = str(BASE_DIR / "uploads")
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
    # Email delivery through the Brevo SMTP relay (587 = STARTTLS, 465 = SSL).
    # Put SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS and SMTP_FROM in backend/.env.
    # The legacy SMTP_USERNAME / SMTP_PASSWORD / SMTP_FROM_EMAIL names are still accepted.
    smtp_host: str = Field(default="smtp-relay.brevo.com", validation_alias=AliasChoices("SMTP_HOST"))
    smtp_port: int = Field(default=587, validation_alias=AliasChoices("SMTP_PORT"))
    smtp_user: str = Field(default="", validation_alias=AliasChoices("SMTP_USER", "SMTP_USERNAME"))
    smtp_pass: str = Field(default="", validation_alias=AliasChoices("SMTP_PASS", "SMTP_PASSWORD"))
    # Must be an address verified by the Brevo account, otherwise delivery is rejected.
    smtp_from: str = Field(default="", validation_alias=AliasChoices("SMTP_FROM", "SMTP_FROM_EMAIL"))
    smtp_from_name: str = Field(default="AI Grievance Management System", validation_alias=AliasChoices("SMTP_FROM_NAME"))
    # Implicit TLS instead of STARTTLS; only needed for port 465.
    smtp_secure: bool = Field(default=False, validation_alias=AliasChoices("SMTP_SECURE"))

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
