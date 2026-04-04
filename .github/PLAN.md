# Active Plan

Last updated: 2026-04-04

## Current objective
Set up the full project repo: documentation, Claude ecosystem files, then implementation.

## Checklist

### Phase 0 — Documentation & Repo Structure
- [x] `.gitignore`
- [x] `CLAUDE.md`
- [x] `README.md`
- [x] `.github/PLAN.md` (this file)
- [x] `.github/DECISIONS.md`
- [x] `.github/NOTES.md`
- [x] `.claude/settings.json`
- [x] `.claude/agents/data-analyst.md`
- [x] `.claude/agents/sql-validator.md`
- [x] `.claude/skills/explain-chart.md`
- [x] `.claude/skills/new-chart.md`
- [x] `.claude/skills/schema-check.md`
- [x] `.claude/skills/cxo-summary.md`

### Phase 1 — Foundation
- [ ] Write `data/load_who.py` — calls WHO GHO API for 6 indicators, filters to 5 countries (RWA/KEN/UGA/ETH/TZA), loads into `data/who_health.duckdb`
- [ ] Run ingestion, verify row counts and NULL rates per indicator
- [ ] Populate `data/schema_registry.json` with real column names + WHO indicator definitions
- [ ] Initialize `backend/pyproject.toml`
- [ ] Create directory skeleton (`backend/`, `dashboard/`, `data/`, `.streamlit/`)

### Phase 2 — Backend Core
- [ ] `backend/config.py` — Pydantic settings
- [ ] `backend/models.py` — IntentResult, ChartSpec, ChatRequest, ChatResponse
- [ ] `backend/database.py` — DuckDB read-only connection + execute_query()
- [ ] `backend/sql_validator.py` — allowlist validation
- [ ] `backend/provenance.py` — read/write provenance.json
- [ ] `backend/schema_loader.py` — build_schema_digest() for prompt caching
- [ ] `backend/static_charts.py` — 6 pre-built CXO chart definitions
- [ ] `backend/main.py` — FastAPI app: GET /charts, GET /charts/{id}, POST /chat

### Phase 3 — Claude API Integration
- [ ] `backend/intent_classifier.py` — structured output → IntentResult
- [ ] `backend/chat_orchestrator.py` — agentic tool-calling loop
- [ ] `backend/handlers/explain_chart.py`
- [ ] `backend/handlers/new_analysis.py` (streaming)
- [ ] `backend/handlers/reject.py`
- [ ] `backend/hooks/inject_schema_digest.py` — PreToolUse hook
- [ ] `backend/hooks/save_provenance.py` — PostToolUse hook

### Phase 4 — Dashboard
- [ ] Run `/ui-ux-pro-max plan` for palette + Plotly theme
- [ ] `.streamlit/config.toml` — Streamlit theme
- [ ] `dashboard/theme.py` — Plotly color constants + chart template
- [ ] `dashboard/api_client.py` — typed httpx calls to FastAPI
- [ ] `dashboard/components/chart_renderer.py`
- [ ] `dashboard/components/chart_card.py`
- [ ] `dashboard/components/chat_panel.py`
- [ ] `dashboard/app.py` — main Streamlit app

### Phase 5 — Polish + Demo Prep
- [ ] `data/benchmark_questions.json` — 20 test questions (4 intent types)
- [ ] Run all 20 benchmark questions, fix failures
- [ ] Error states: loading spinners, rejection messages, API errors
- [ ] Prepare 5-minute demo script
- [ ] Final README update with screenshots

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
