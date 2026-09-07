# Backend

This folder contains the FastAPI backend for the PetCare platform.

Run locally:

```bash
export $(cat .env | xargs)
uvicorn backend.app.main:app --reload --port 8000
```
