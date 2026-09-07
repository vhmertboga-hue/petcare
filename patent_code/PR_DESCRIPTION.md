Feature: Business Panel, Pet Hotel & Reservations

Summary
-------
This branch adds the core backend support for a professional Business Panel to manage verified businesses (veterinary clinics, vets, pet hotels, daycares). It includes:

- `Business` model (owner, status: pending/verified/rejected/suspended, profile data)
- `PetHotel` linked to `Business`
- `Reservation` model and availability checks
- Business application endpoints for owners
- Admin endpoints to list pending applications and change status
- Alembic migration to create `businesses` and `reservations` tables and alter `files` table

Files changed
--------------
- backend/app/models/business.py (new)
- backend/app/models/pet_hotel.py (updated)
- backend/app/models/reservation.py (new)
- backend/app/services/business_service.py (new)
- backend/app/services/reservation_service.py (new)
- backend/app/api/api_v1/endpoints/businesses.py (new)
- backend/app/api/api_v1/endpoints/admin_businesses.py (new)
- backend/backend/alembic/versions/0001_add_business_and_reservation.py (new)
- backend/alembic/env.py, backend/alembic.ini (new)

What to review
--------------
- Model definitions and relationships
- API endpoints and access control (owners vs admin)
- Alembic migration content

How to apply migration locally (recommended)
------------------------------------------------
Set your database URL (Postgres recommended for production/staging):

```bash
export DATABASE_URL=postgresql+asyncpg://<user>:<pass>@localhost:5432/petcare
cd patent_code/backend
alembic -c alembic.ini upgrade head
```

Notes for CI and tests
----------------------
- The repo includes a test `conftest.py` that creates an in-memory SQLite DB by default for unit tests. Ensure `pytest` runs from repository root so imports resolve correctly.
- To run tests locally:

```bash
cd patent_code
pytest -q
```

Known issues and environment notes
---------------------------------
- While implementing this feature I resolved multiple metadata/import issues (duplicate Base declarations and duplicate `User` class definitions). Tests in different local environments may still encounter import path issues if `PYTHONPATH` is set inconsistently. If you see `Table 'users' is already defined` errors, check that `PYTHONPATH` is not set to a conflicting value and run `pytest` from repository root.
- If CI runs against Postgres, migrations should be applied in CI before tests run.

Checklist (what I did)
----------------------
- [x] Add `Business` model and link with owner
- [x] Link `PetHotel` to `Business`
- [x] Add `Reservation` model + availability service
- [x] Add owner-facing business endpoints
- [x] Add admin endpoints for verifying businesses
- [x] Create Alembic migration stub for new tables
- [x] Fix model import/metadata issues encountered during development

Next recommended steps
----------------------
1. Apply migration in staging/CI and run full test suite.
2. Harden reservation concurrency (DB-level locking or serializable transactions).
3. Add business dashboard endpoints for revenue/commission reporting.
4. Add frontend business panel (owner UI) and admin review UI.
