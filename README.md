# Nivaran — AI Grievance System

This project keeps the original AI engine, backend and frontend and connects them into one flow.

## Start

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

In VS Code, choose **Nivaran API (FastAPI)** from Run and Debug. Do not use **Run Python File** on `backend/app/routes.py`; that file defines an API router and is not the server entry point. The router must be imported as `app.routes` by `app.main` while `backend` is the working directory.

Open:
- `http://127.0.0.1:8765/` — frontend
- `http://127.0.0.1:8765/docs` — API docs
- `http://127.0.0.1:8765/health` — health/config status

## Flow

Mobile number/password → JWT login → first-time citizen profile → complaint text/location/photo → AI preview → ticket/category/severity/priority/department/resolution time → citizen submit → notifications → officer workflow → resolution → citizen feedback → admin analytics.

## AI

The existing AI modules remain in `AI/`. The backend adapter calls `AI/prediction/ai_engine.py` and does not automatically add unverified production complaints to the training dataset.

## Account access

Citizens register with a mobile number and password, then complete profile setup. Returning users log in with the same credentials. Passwords are stored as Argon2 hashes.

## Frontend

The original frontend remains under `smart-grievance-frontend/frontend/`. Backend serving was added so the same files are available directly from port 8765. Additional integration scripts and officer/admin pages were added; existing pages/assets were not deleted.
