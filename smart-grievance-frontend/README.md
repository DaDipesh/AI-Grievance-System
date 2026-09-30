# Nivaran Frontend

The original frontend remains under `frontend/` and is served by FastAPI during local development.

## Run

From the project root:

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765/`. The shared API client uses `http://127.0.0.1:8765/api/v1` when served from the backend or from a local frontend development server. For a separately hosted frontend, set `window.SG_API_BASE_URL` before `js/api.js` loads or provide a `<meta name="sg-api-base" content="http://127.0.0.1:8765/api/v1">` tag.

Registration and login use mobile number/password through the FastAPI API. Passwords are hashed by the backend; the first registration opens profile setup.
