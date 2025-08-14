# WealthWise Backend (FastAPI)

A combined Splitwise-style expense-sharing + wealth monitoring API.

## Tech
- FastAPI, SQLAlchemy ORM
- JWT auth (python-jose)
- SQLite (dev) / Postgres (prod)
- ENV config via `.env`
- Swagger UI at `/docs`

## Quickstart (Dev)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# (Optional) edit .env
uvicorn app.main:app --reload
```
Backend will run on `http://127.0.0.1:8000`.

## Postgres (Prod)
Set `DATABASE_URL` in `.env`, e.g.:
```
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/wealthwise
```
Run with a production server (e.g., uvicorn/gunicorn).

## Seeding Test Data
```bash
python seed.py
```
This creates demo users, a group, expenses, and dummy wealth holdings.

## Project Structure
```
app/
  core/ (config, db)
  auth/ (jwt utils, dependencies)
  models/ (SQLAlchemy models)
  schemas/ (Pydantic DTOs)
  routers/ (auth, groups, payments, integrations, wealth)
  main.py
seed.py
```

## CORS
Configure allowed origins in `.env` (`CORS_ORIGINS`).

## Integrations
- Zerodha: placeholder OAuth endpoints for token storage. Plug in real flow later.
- Account Aggregator (AA): placeholder connect/refresh endpoints.

