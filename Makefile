# Run from the repo root. All commands set PYTHONPATH=. so that
# 'backend' and 'dashboard' are importable as packages.

.PHONY: load backend dashboard frontend install install-frontend test test-ui

# Install all Python dependencies into the active virtualenv
install:
	pip install -r requirements.txt

# Install Node.js dependencies for the React frontend
install-frontend:
	cd frontend && npm install

# Populate the WHO database (run once before starting the backend)
load:
	PYTHONPATH=. python data/load_who.py

# Start the FastAPI backend
backend:
	PYTHONPATH=. uvicorn backend.main:app --reload

# Start the React frontend (Vite dev server on :3000, proxies /charts and /chat to :8000)
frontend:
	cd frontend && npm run dev

# Start the Streamlit dashboard (legacy)
dashboard:
	PYTHONPATH=. streamlit run dashboard/app.py

# Run backend + data unit tests (no servers needed)
test:
	PYTHONPATH=. pytest tests/backend tests/data -v

# Run Playwright UI tests (requires: make backend and make dashboard running)
test-ui:
	PYTHONPATH=. pytest tests/dashboard -v
