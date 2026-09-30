import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.database import init_db
from app.i18n import message
from app.routes import router
from app.services.email_service import smtp_server_label

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("grievance.api")

app = FastAPI(
    title="Nivaran AI Grievance System API",
    version="4.0.0",
    description="Nivaran: citizen registration, AI grievance analysis, routing, tracking, officer workflow, notifications, feedback and admin analytics.",
)
settings = get_settings()
app.add_middleware(CORSMiddleware, allow_origins=["*"] if settings.environment.lower() in {"development", "dev", "local"} else [], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api/v1")

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "smart-grievance-frontend" / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")

@app.on_event("startup")
def startup() -> None:
    init_db()
    logger.info("AI Grievance System started with password authentication.")
    # Report the relay host and port only; SMTP credentials are never logged.
    logger.info("Email notifications use SMTP server %s", smtp_server_label(get_settings()))

@app.get("/")
def root():
    if FRONTEND_DIR.joinpath("login.html").exists():
        return RedirectResponse(url="/login.html", status_code=307)
    return {"name": "Nivaran AI Grievance System", "version": app.version, "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok", "authentication": "password"}

# Serve every existing frontend page without deleting or relocating the original frontend.
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

def language_from(request: Request) -> str:
    return "hi" if request.headers.get("accept-language", "").lower().startswith("hi") else "en"

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": "Please check the request fields." if language_from(request) == "en" else "कृपया अनुरोध की जानकारी जाँचें।"})

@app.exception_handler(SQLAlchemyError)
async def database_error(request: Request, exc: SQLAlchemyError):
    logger.exception("Database operation failed")
    return JSONResponse(status_code=500, content={"detail": message("server_error", language_from(request))})

@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception):
    logger.exception("Unhandled API error")
    return JSONResponse(status_code=500, content={"detail": message("server_error", language_from(request))})
