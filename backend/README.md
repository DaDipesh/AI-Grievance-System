# AI Grievance Management System — Backend + AI

This folder contains the FastAPI backend and the existing AI grievance engine. It supports mobile number/password authentication, profile setup, multilingual complaint analysis, category/severity/priority prediction, department routing, resolution-time prediction, evidence upload, duplicate detection, officer workflow, status history, notifications, feedback and admin analytics.

## Start locally

From `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Open:

- `http://127.0.0.1:8765/docs`
- `http://127.0.0.1:8765/health`

If port 8765 is already occupied, stop the existing Uvicorn process or use another free port.

Do not run `app/routes.py` as a Python file. It is an imported FastAPI router module, not a server entry point; running it directly breaks the `app.*` package imports (for example, `ModuleNotFoundError: No module named 'app'`). Start `app.main:app` through Uvicorn as shown above. The workspace also includes a VS Code **Nivaran API (FastAPI)** debug configuration that uses the correct module and working directory.

## Database

The included development `.env` uses SQLite for a zero-configuration demo. Existing SQLite databases are upgraded at startup with the required new columns and tables.

For PostgreSQL, set `DATABASE_URL` in `.env`, for example:

```text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
```

For production, use Alembic migrations, HTTPS, a strong JWT secret, a real SMS provider, restricted CORS and a managed PostgreSQL database.

## Authentication

Citizens register with a mobile number and password, then complete their profile once. Passwords are stored as Argon2 hashes. Login uses `POST /api/v1/auth/login`; registration uses `POST /api/v1/auth/register`.

Registration defaults to the citizen role. Admin registration requires the configured `ADMIN_REGISTRATION_ID`. Officer registration requires the ID configured for the selected department (`OFFICER_WATER_ID`, `OFFICER_ELECTRICITY_ID`, `OFFICER_STREET_LIGHT_ID`, `OFFICER_ROAD_ID`, `OFFICER_HEALTHCARE_ID`, `OFFICER_SANITATION_ID`, `OFFICER_DRAINAGE_ID`, or `OFFICER_ENVIRONMENT_ID`). These values belong only in backend `.env`; empty values disable registration for that role/department. The API checks the exact ID and its expected length (16 characters for admin, 12 for officers). Admin accounts can view all complaints and the officer directory.

## Main API flow

1. `POST /api/v1/auth/register` or `POST /api/v1/auth/login`
2. Citizen: `PUT /api/v1/users/me/profile` (after registration, first login only)
3. Officer/admin: `PUT /api/v1/users/me/staff-profile` (after registration, first login only; officer department is fixed by the validated registration ID)
4. `POST /api/v1/complaints/evidence` (optional)
5. `POST /api/v1/complaints`
6. `GET /api/v1/complaints`
7. `GET /api/v1/complaints/{complaint_id}`
8. `GET /api/v1/complaints/{complaint_id}/history`
9. Officer: `GET /api/v1/officer/complaints`
10. Officer: `PUT /api/v1/officer/complaints/{complaint_id}/status`
11. Admin: `PUT /api/v1/admin/complaints/{complaint_id}/assign`
12. Admin: `GET /api/v1/admin/complaints`
13. Admin: `GET /api/v1/admin/health-summary`
14. `GET /api/v1/notifications`
15. Citizen: `POST /api/v1/complaints/{complaint_id}/feedback` after resolution

## Complaint response

The response now includes the database `id` as well as the public `ticket_number`, so the frontend can safely call the status/history/feedback endpoints without guessing the complaint ID.

## Development demo accounts

`POST /api/v1/dev/seed-demo-users` is available only when `ENVIRONMENT=development`. It creates demo admin/officer users with password `Demo@12345`. It is disabled outside development.

Existing users receive a nullable password hash column during startup migration. Accounts that do not yet have a password hash need an administrator to provision their password before password login can be used.

## Important AI note

Production complaints are not automatically appended to the training CSV at intake. When an officer resolves a complaint, a verified record is added to `AI/dataset/verified_complaints.csv` for future retraining. The resolution model is a demo/synthetic model and should be retrained on real historical government data before production use.
