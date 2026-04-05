# Run from the repo root. All commands set PYTHONPATH=. so that
# 'backend' and 'dashboard' are importable as packages.

.PHONY: load backend dashboard install test test-ui

# Install all dependencies into the active virtualenv
install:
	pip install -r requirements.txt

# Populate the WHO database (run once before starting the backend)
load:
	PYTHONPATH=. python data/load_who.py

# Start the FastAPI backend
backend:
	PYTHONPATH=. uvicorn backend.main:app --reload

# Start the Streamlit dashboard
dashboard:
	PYTHONPATH=. streamlit run dashboard/app.py

# Run backend + data unit tests (no servers needed)
test:
	PYTHONPATH=. pytest tests/backend tests/data -v

# Run Playwright UI tests (requires: make backend and make dashboard running)
test-ui:
	PYTHONPATH=. pytest tests/dashboard -v
