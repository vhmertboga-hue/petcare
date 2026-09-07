## Summary

Add Business Panel support: `Business`, `PetHotel`, `Reservation`, owner and admin endpoints, and Alembic migration.

## Testing

- Apply migrations: `alembic -c backend/alembic.ini upgrade head`
- Run tests: `pytest -q`

## Notes

- This PR includes fixes for model import/metadata issues. If you see duplicate-table errors locally, ensure tests are run from repository root and `PYTHONPATH` is not interfering.

## Checklist
- [ ] Migration applied in staging
- [ ] CI tests passing
- [ ] Frontend owner/admin panels wired to these endpoints
