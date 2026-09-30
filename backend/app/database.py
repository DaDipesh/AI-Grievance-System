from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
database_url = make_url(settings.database_url)
if database_url.drivername in {"postgres", "postgresql"}:
    # Render provides postgresql:// URLs; this project installs psycopg v3.
    database_url = database_url.set(drivername="postgresql+psycopg")
if database_url.drivername.startswith("sqlite") and database_url.database not in {None, ":memory:"}:
    database_path = Path(database_url.database)
    if not database_path.is_absolute():
        database_url = database_url.set(database=str((Path(__file__).resolve().parents[1] / database_path).resolve()))
connect_args = {"check_same_thread": False} if database_url.drivername.startswith("sqlite") else {}
engine = create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _add_missing_columns(table: str, columns: dict[str, str]) -> None:
    inspector = inspect(engine)
    if not inspector.has_table(table):
        return
    existing = {c["name"] for c in inspector.get_columns(table)}
    with engine.begin() as conn:
        for name, sql_type in columns.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {sql_type}"))


def init_db() -> None:
    # Hackathon/local migration layer. For production, replace with Alembic.
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    _add_missing_columns("users", {
        "password_hash": "VARCHAR(255)",
        "gender": "VARCHAR(20)",
        "city": "VARCHAR(120)",
        "state": "VARCHAR(120)",
        "district": "VARCHAR(120)",
        "village": "VARCHAR(120)",
        "pincode": "VARCHAR(12)",
        "address": "VARCHAR(500)",
        "latitude": "DOUBLE PRECISION",
        "longitude": "DOUBLE PRECISION",
        "profile_photo_data": "TEXT",
    })

    _add_missing_columns("complaints", {
        "district": "VARCHAR(120)",
        "state": "VARCHAR(120)",
        "location_source": "VARCHAR(20)",
        "language": "VARCHAR(12)",
        "estimated_resolution_hours": "DOUBLE PRECISION",
        "estimated_resolution_days": "DOUBLE PRECISION",
        "evidence_path": "VARCHAR(500)",
        "ai_response": "TEXT",
        "category_verified": "VARCHAR(120)",
        "resolution_hours_actual": "DOUBLE PRECISION",
        "category_source": "VARCHAR(32)",
        "ml_confidence": "DOUBLE PRECISION",
        "team": "VARCHAR(120)",
        "routing_status": "VARCHAR(32)",
        "duplicate_flag": "BOOLEAN DEFAULT FALSE",
        "duplicate_similarity": "DOUBLE PRECISION",
        "duplicate_existing_id": "VARCHAR(120)",
        "status_note": "VARCHAR(1000)",
        "resolved_at": "TIMESTAMP",
        "sla_due_at": "TIMESTAMP",
        "escalated_at": "TIMESTAMP",
        "escalation_level": "INTEGER DEFAULT 0",
        "updated_at": "TIMESTAMP",
    })

    _add_missing_columns("complaint_drafts", {
        "complaint_id": "INTEGER",
    })

    # Existing databases may have NULL updated_at after migration; the app
    # updates it on every write, so this is safe for both SQLite and PostgreSQL.
    with engine.begin() as conn:
        if inspect(engine).has_table("complaints"):
            conn.execute(text("UPDATE complaints SET duplicate_flag = FALSE WHERE duplicate_flag IS NULL"))
            conn.execute(text("UPDATE complaints SET updated_at = created_at WHERE updated_at IS NULL"))
            conn.execute(text("UPDATE complaints SET escalation_level = 0 WHERE escalation_level IS NULL"))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
