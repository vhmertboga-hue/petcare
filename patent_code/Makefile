.PHONY: help run test build

help:
	@echo "Makefile commands:"
	@echo "  make run    - Run backend with uvicorn"
	@echo "  make test   - Run pytest in backend"

run:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q backend/tests
