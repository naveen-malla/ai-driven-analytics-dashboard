# Active Plan

Last updated: 2026-04-05

## Current objective
Phase 3 — Wire up real Claude API integration (intent classifier, tool-calling loop, handlers).
After that: run data pipeline to populate DuckDB, then smoke-test full stack end-to-end.

## Checklist

### Phase 0 — Documentation & Repo Structure
- [x] `.gitignore`
- [x] `CLAUDE.md`
- [x] `README.md`
- [x] `.github/PLAN.md` (this file)
- [x] `.github/DECISIONS.md`
- [x] `.github/NOTES.md`
- [x] `.github/INTEGRATION_CONTRACTS.md`
- [x] `.github/personas/naveen.md`, `pathey.md`, `marco.md`
- [x] `.github/HACKATHON_LESSONS.md`
- [x] `.claude/settings.json`
- [x] `.claude/agents/data-analyst.md` (WHO GHO)
- [x] `.claude/agents/sql-validator.md` (WHO GHO)
- [x] `.claude/skills/explain-chart.md`
- [x] `.claude/skills/new-chart.md`
- [x] `.claude/skills/schema-check.md`
- [x] `.claude/skills/cxo-summary.md`
- [x] `.claude/skills/demo-review.md`
- [x] `.claude/skills/hackathon-brief.md`
- [x] `.claude/skills/to-showcase.md`

### Phase 1 — Foundation
- [x] Write `data/load_who.py` — calls WHO GHO API for 6 indicators, 5 countries
- [ ] **NEXT**: Run ingestion (`python data/load_who.py`) — verify row counts and NULL rates
- [x] `data/schema_registry.json` — full table/column/join definitions
- [x] `backend/pyproject.toml`
- [x] `requirements.txt`
- [x] Directory skeleton (`backend/`, `dashboard/`, `data/`, `.streamlit/`)

### Phase 2 — Backend Core
- [x] `backend/config.py` — Pydantic settings
- [x] `backend/models.py` — IntentResult, ChartSpec, ChatRequest, ChatResponse
- [x] `backend/database.py` — DuckDB read-only connection + execute_query()
- [x] `backend/sql_validator.py` — 5-check allowlist validation
- [x] `backend/provenance.py` — read/write provenance.json
- [x] `backend/schema_loader.py` — build_schema_digest() for prompt caching
- [x] `backend/static_charts.py` — 6 pre-built CXO chart definitions with WHO SQL
- [x] `backend/main.py` — FastAPI app: GET /charts, GET /charts/{id}, POST /chat (stub)
- [x] `backend/handlers/reject.py` — real refusal message

### Phase 3 — Claude API Integration
- [ ] `backend/intent_classifier.py` — replace stub with structured output → IntentResult
- [ ] `backend/chat_orchestrator.py` — replace stub with agentic tool-calling loop
- [ ] `backend/handlers/explain_chart.py` — real implementation
- [ ] `backend/handlers/new_analysis.py` — real implementation (streaming)
- [ ] `.env` file with `ANTHROPIC_API_KEY` (not committed — add to .gitignore)

### Phase 4 — Dashboard
- [x] Run ui-ux-pro-max → data-dense dashboard, blue/amber palette
- [x] `dashboard/DESIGN_BRIEF.md` — CXO narrative and chart ordering rationale
- [x] `.streamlit/config.toml` — Streamlit theme
- [x] `dashboard/theme.py` — Plotly color constants + chart template
- [x] `dashboard/api_client.py` — typed httpx calls to FastAPI
- [x] `dashboard/components/chart_card.py` — Plotly chart renderer, warm colors for "lower=better"
- [x] `dashboard/components/chat_panel.py` — chat UI with session state
- [x] `dashboard/app.py` — main Streamlit app, 2×3 chart grid + chat panel
- [ ] End-to-end smoke test: run backend + dashboard with real DuckDB data

### Phase 5 — Polish + Demo Prep
- [x] `data/benchmark_questions.json` — 10 test questions (3 intent types) — expand to 20 after Phase 3
- [ ] Run all benchmark questions against live Claude API, fix failures
- [ ] Error states: loading spinners, rejection messages, API errors
- [ ] Prepare 5-minute demo script
- [ ] Final README update with screenshots
- [ ] Run `/demo-review` — all checks PASS

### Phase 6 — Hackathon Prep

> Goal: Extract the minimal starter repo, confirm 3-person parallel workflow, produce day-of setup checklist.

#### 6a — Parallel workstream breakdown (zero git conflict risk)

| Person | Owns | First 30-min task |
|--------|------|-------------------|
| Naveen | `backend/`, `.claude/` | `backend/config.py`, `backend/database.py`, confirm GET /charts returns 200 |
| Pathey | `data/` | Connect Kasha data, run `load_kasha.py`, populate `schema_registry.json` — everyone waits on this |
| Marco | `dashboard/`, `.streamlit/` | Run `/ui-ux-pro-max plan`, create `.streamlit/config.toml` and `dashboard/theme.py` |

Integration merge order: `pathey/data` → `naveen/backend` → `marco/dashboard`

#### 6b — Sync schedule
| Time | Format | Purpose |
|------|--------|---------|
| Hour 0 | 5 min | Confirm everyone unblocked, Pathey has schema |
| Hour 1 | 5 min | Pathey shares final `schema_registry.json` — Naveen and Marco unblock |
| Hour 4 | 15 min | Integration checkpoint — wire dashboard ↔ API ↔ DB end-to-end |
| Hour 5.5 | 15 min | Demo dry run — run `/demo-review`, fix any blockers |

#### 6c — Keep vs strip checklist for Kasha starter repo
- [ ] Confirm all 9 DECISIONS.md items are portable (data-source-agnostic)
- [ ] Replace CMS column references with `[REPLACE WITH KASHA]` placeholders
- [ ] Remove `data/raw/`, `data/cms_hospital.duckdb`, `data/load_cms.py`
- [ ] Replace CMS metric table in `CLAUDE.md` with Kasha metric placeholders
- [ ] Update README for Kasha context
- [ ] Test: fresh `git clone` + `.env` setup → `uvicorn` runs without error

#### 6d — Phase 6 completion checklist
- [ ] Run `/demo-review` — all checks PASS
- [ ] Run `/hackathon-brief` — output is accurate and current
- [ ] Run `/to-showcase` — project text converted from prep framing to showcase framing
- [ ] Create `kasha-insights-starter/` repo with stripped content
- [ ] Confirm starter repo passes fresh setup test on a clean machine
- [ ] Share `HACKATHON_SETUP.md` with Marco and Pathey — confirm they can follow it independently
- [ ] Schedule day-before kickoff call with Marco and Pathey
