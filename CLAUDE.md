# AI Healthcare Analytics Dashboard — Project Memory

## What this project is
A CXO-facing healthcare analytics dashboard with an AI chat copilot.
- **Static dashboard**: 6 pre-built executive charts from CMS Hospital Compare public data
- **AI chat**: two modes — explain/modify an existing chart, or generate a new analysis
- **Governed copilot**: the AI works within strict boundaries (read-only SQL, known schema, refusal logic)

## Hackathon Context

This is a **rehearsal project**. The real target is a 6-hour company hackathon the week of 2026-04-06.

### Real hackathon target
**Kasha Unified Insights Platform** — a governed analytics copilot over Kasha's internal databases (distribution, product, last-mile health access data), replacing ad-hoc SQL requests to the data team with a self-service CXO interface. Kasha (kasha.co) is a Rwanda-based digital health and pharmaceutical distribution startup expanding across Africa. This prep project proves the architecture pattern using safe public data (CMS Hospital Compare) before it is rebuilt with Kasha's actual data.

### Team roles and directory ownership (hackathon day)
| Person | Role | Owns | Never touches |
|--------|------|------|---------------|
| Naveen | Backend / AI | `backend/`, `.claude/` | `dashboard/`, `data/` |
| Pathey | Data / ML | `data/` | `backend/`, `dashboard/` |
| Marco | UI / UX | `dashboard/`, `.streamlit/` | `backend/`, `data/` |

Zero directory overlap by design — no merge conflicts during the 6-hour build.

**Integration contracts** (the only cross-person coordination points):
- `backend/main.py` GET /charts response shape ↔ `dashboard/api_client.py` — agree before coding
- `data/schema_registry.json` column names ↔ `backend/schema_loader.py` — Pathey finalizes first
- `backend/static_charts.py` chart IDs ↔ `dashboard/components/chart_card.py` — agree on keys before coding

### What will be stripped for the hackathon starter repo
**Strip**: `data/raw/`, `data/cms_hospital.duckdb`, `data/load_cms.py`, `data/schema_registry.json`, `data/benchmark_questions.json`, CMS metric definitions from this file, CMS column references in `backend/static_charts.py` and `backend/schema_loader.py`

**Keep**: All architecture scaffolding — `backend/` module structure, `dashboard/` components, `.claude/` agents/skills/settings, `HACKATHON_SETUP.md`, `.github/DECISIONS.md` (all 9 decisions are data-source-agnostic)

## Claude usage split
- **Claude Code** (this tool, subscription): used for development — scaffolding, skills, agents, hooks
- **Claude API** (`ANTHROPIC_API_KEY`): used only inside the running app — intent classification, tool calling, prompt caching

## Dataset
- **Source**: WHO Global Health Observatory (GHO) public API — `https://ghoapi.azureedge.net/api/`
- **DuckDB file**: `data/who_health.duckdb` (read-only in production, git-ignored)
- **Schema registry**: `data/schema_registry.json` (business definitions + allowed joins)
- **Tables**: `countries`, `indicators`, `country_data`
- **Join keys**: `country_data` joins `countries` on `country_code`; joins `indicators` on `indicator_code`
- **Countries**: Rwanda (RWA), Kenya (KEN), Uganda (UGA), Ethiopia (ETH), Tanzania (TZA) — Kasha's core markets
- **Ingestion script**: `data/load_who.py` — calls GHO API per indicator, filters to 5 countries, loads into DuckDB

## Metric definitions
| Metric | WHO Indicator Code | Definition | Direction |
|--------|-------------------|-----------|-----------|
| contraceptive_prevalence | FP_CXUS_W_CURR | % women 15–49 using any contraceptive method | Higher = better |
| maternal_mortality_ratio | MDG_0000000025 | Maternal deaths per 100,000 live births | Lower = better |
| antenatal_care_coverage | MDG_0000000031 | % pregnant women with 4+ antenatal visits | Higher = better |
| skilled_birth_attendance | MDG_0000000032 | % births attended by skilled health personnel | Higher = better |
| under5_mortality_rate | MDG_0000000001 | Deaths per 1,000 live births under age 5 | Lower = better |
| hiv_prevalence | HIV_0000000026 | % adults 15–49 living with HIV | Lower = better |

**Critical**: WHO GHO values may be NULL for some country/year combinations — treat as missing data, not zero. Always filter `WHERE value IS NOT NULL`.

## SQL rules (enforced by sql_validator.py)
- SELECT only — no INSERT, UPDATE, DELETE, CREATE, DROP, TRUNCATE, COPY
- No semicolons inside a query (blocks multi-statement injection)
- All referenced tables must exist in `data/schema_registry.json`
- LIMIT clause required, max 500 rows
- No arbitrary shell or file access

## Git commit rules
- Commit messages must not reference Kasha, the hackathon, prep work, internal team names (Marco, Pathey), or personal context
- Write every commit as if this is a standalone public showcase project
- Never include "Co-Authored-By" or AI tool references in commit messages
- Follow conventional commits: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`

## Coding standards
- Python 3.12, FastAPI, DuckDB, Anthropic SDK (`anthropic`)
- Pydantic v2 for all models and settings
- Frontend: Streamlit + Plotly (Python-only, no JavaScript)
- Model: `claude-sonnet-4-6` for all Claude API calls
- All DB access through `backend/database.py` — never instantiate DuckDB directly elsewhere
- Chart provenance persisted to `data/provenance.json` via `backend/provenance.py`

## Architecture layers
```
dashboard/app.py          ← Streamlit UI
    ↓ httpx
backend/main.py           ← FastAPI (routes: GET /charts, GET /charts/{id}, POST /chat)
    ↓
backend/chat_orchestrator.py  ← routes intent to handlers
    ↓
backend/intent_classifier.py  ← Claude structured output → IntentResult
backend/handlers/             ← explain_chart, new_analysis, reject
    ↓
backend/sql_validator.py      ← blocks before DuckDB
backend/database.py           ← DuckDB read-only
```

## What the AI may answer
- Trends over time per country and indicator
- Country comparisons and rankings by health metric
- Regional cohort splits (by WHO region or income group)
- Period-over-period changes in any indicator
- Top/bottom performing countries by metric

## What the AI must reject
- Questions requiring data not in schema: costs, supply chain volumes, product sales, staffing, diagnoses
- Causal inference ("why" questions that require attribution)
- Forecasting or predictions beyond available data years
- Anything referencing specific patient or individual records
- Questions entirely off-topic from public health metrics

## Running the app

Always use `PYTHONPATH=.` from repo root so `backend` and `dashboard` are importable:
```bash
make load       # populate WHO database (run once)
make backend    # FastAPI on :8000
make dashboard  # Streamlit on :8501
```

## Testing rules (enforced for all code changes)

These apply to Naveen, Pathey, Marco, and any AI agent working in this repo.

### The rule
**No feature is complete until its tests pass.** Writing code and declaring it done without running tests is not acceptable. Agents must run tests after writing code and loop until green before committing.

### Test layout
```
tests/
├── conftest.py                  # shared fixtures: in-memory test DuckDB, mock data
├── backend/
│   ├── test_sql_validator.py    # all 5 validation checks + edge cases
│   ├── test_static_charts.py    # SQL structure, chart IDs, required fields
│   ├── test_api.py              # FastAPI routes via TestClient
│   ├── test_schema_loader.py    # schema registry parsing
│   └── test_database.py        # execute_query, missing-DB error
├── data/
│   └── test_schema_registry.py # JSON structure matches integration contracts
└── dashboard/
    └── test_ui.py              # Playwright: page loads, 6 charts render, chat present
```

### Backend + data tests (pytest)
- Run: `PYTHONPATH=. pytest tests/backend tests/data -v`
- Use in-memory DuckDB with fixture data — never depend on the real `who_health.duckdb`
- Every new backend function gets at least one test before the feature is committed
- Tests must pass before any `git commit` on `backend/` or `data/` files

### Dashboard tests (Playwright)
- Run: `PYTHONPATH=. pytest tests/dashboard -v` (requires both servers running)
- Marco's UI changes are not complete until Playwright confirms: page loads, all 6 chart cards render, "Ask about this chart" button exists on each, chat panel accepts input
- Every new UI component or layout change needs a corresponding Playwright check

### Agent workflow for code changes
1. Write the code
2. Write the test for it
3. Run the test: `PYTHONPATH=. pytest <test file> -v`
4. If it fails — fix the code, not the test (unless the test itself is wrong)
5. Loop until green
6. Only then commit

### Hackathon day
- Same rules apply under time pressure
- Pathey: run `pytest tests/data` after producing `schema_registry.json`
- Naveen: run `pytest tests/backend` after each backend module
- Marco: run Playwright after each UI component — the test tells him it works before he calls it done
- Integration tests run after each workstream merge

## File locations
- Backend source: `backend/`
- Dashboard source: `dashboard/`
- Data files: `data/`
- Tests: `tests/`
- Claude ecosystem: `.claude/` (agents, skills, settings)
- Active plan: `.github/PLAN.md`
- Architecture decisions: `.github/DECISIONS.md`
- Working notes: `.github/NOTES.md`
