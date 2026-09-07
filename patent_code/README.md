# PetCare Platform (scaffold)

Purpose: provide a production-ready scaffold for the PetCare project (backend, web, mobile, admin).

Tech stack (PHASE 1):
- Backend: FastAPI (Python)
- Database: PostgreSQL (dev)
- Cache/Queue: Redis (dev)
- Storage: MinIO (dev)
- CI: GitHub Actions
- Containerization: Docker / Docker Compose
- Linting/Formatting: black, isort, flake8, mypy

Quickstart
1. Copy `.env.example` to `.env` and update values.
2. Start dev stack:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

3. Create virtualenv and install backend deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

4. Run backend (dev):

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Testing

```bash
cd backend
pytest -q
```

Migration

Use Alembic from `backend`:

```bash
cd backend
alembic revision --autogenerate -m "create initial"
alembic upgrade head
```
# PetCare Platform — Backend Scaffold

This repository contains the Phase 1 scaffold for a production-ready backend for the PetCare platform.

Purpose
- Provide a maintainable, secure and testable foundation for further development (auth, features, payments, AI).

Technology stack
- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy + Alembic
- PostgreSQL
- Redis (for caching/queues)
- Docker / Docker Compose
- Pytest, Black, Flake8, Mypy

Setup
1. Copy `.env.example` to `.env` and adjust values.
2. Start dev services via `docker-compose up -d`.
3. Install Python deps: `pip install -r requirements.txt` (prefer a venv).

Development
- Run backend locally: `uvicorn backend.app.main:app --reload --port 8000`
- Run tests: `pytest -q`

Migration
- Initialize migrations: `alembic revision --autogenerate -m "init"`
- Apply migrations: `alembic upgrade head`

Authentication
- Environment variables required for auth/OAuth:
	- `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
	- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `APPLE_CLIENT_ID`, `APPLE_CLIENT_SECRET`
	- Environment değişkenleri
	  - `SECRET_KEY` - JWT secret
	  - `DATABASE_URL` - SQLAlchemy async DB URL
	  - `REDIS_URL` - Redis URL
	  - `AWS_S3_ENDPOINT` - S3 endpoint
	  - `SENTRY_DSN` - optional

See `ARCHITECTURE.md` for system-level details.
