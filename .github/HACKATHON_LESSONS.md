# Hackathon Simulation — Lessons Learned

Date: 2026-04-05
Simulation: 3 isolated agents (Pathey/data, Naveen/backend, Marco/dashboard) working in parallel worktrees

---

## What worked

**Pathey (data)**
- `schema_registry.json` used the exact `"tables"` key that `backend/schema_loader.py` expected.
- Column names (`country_code`, `country_name`, `indicator_code`, `year`, `value`, `sex`) in `schema_registry.json` matched exactly what `backend/static_charts.py` SQL queries SELECT and alias.
- `data/load_who.py` creates the DB at `data/who_health.duckdb` relative to the script's directory, consistent with where the backend config expects it.
- All 6 WHO indicator codes matched between `load_who.py` and `backend/static_charts.py`.
- `schema_registry.json` included `"allowed_joins"` with fully-specified `from_table`, `to_table`, and `on` fields — exactly the structure needed.

**Naveen (backend)**
- `ChartSpec` Pydantic model defined all 9 fields that the integration contract specified: `chart_id`, `title`, `chart_type`, `x_key`, `y_key`, `data`, `metric_definition`, `x_label`, `y_label`.
- `ChartsResponse` wraps charts in a `{"charts": [...]}` envelope, matching what `api_client.py` calls `response_data.get("charts", [])`.
- `ChatResponse` fields (`reply`, `chart`, `intent`) matched exactly what `dashboard/api_client.py` expects.
- `ChatRequest` shape (`message`, `chart_id`) matched what `api_client.py` POSTs.
- All 6 chart IDs in `static_charts.py` matched the contract exactly: `contraceptive_prevalence`, `maternal_mortality`, `antenatal_care`, `skilled_birth`, `under5_mortality`, `hiv_prevalence`.
- `sql_validator.py` enforces SELECT-only, requires LIMIT, blocks multi-statement injection — correct and safe.

**Marco (dashboard)**
- `BACKEND_URL = "http://localhost:8000"` is in exactly one place: `dashboard/api_client.py`. No other dashboard file hardcodes it. Contract 5 honored.
- All 16 constants imported from `dashboard/theme.py` in `chart_card.py` actually exist in `theme.py`. No missing design tokens.
- `chart_card.py` reads `x_key` and `y_key` from the chart spec dict and uses them to extract data values — correctly data-driven rather than hardcoded.
- `LOWER_IS_BETTER_CHARTS = {"maternal_mortality", "under5_mortality", "hiv_prevalence"}` matches the direction column in the integration contract exactly.
- Import paths in `app.py` (`from dashboard.api_client import ...`, `from dashboard.components.chart_card import ...`, `from dashboard.components.chat_panel import ...`) all resolve to files that exist.
- Dashboard has clean graceful degradation — empty list handling, connection error fallbacks, backend-unavailable warning state.

**Merge process**
- All three branches merged with zero conflicts. The directory-ownership split (Pathey=`data/`, Naveen=`backend/`, Marco=`dashboard/`) completely eliminated merge collisions. The design worked as intended.

---

## Contract violations found

| Contract | Violation | Impact | Fix Applied |
|---|---|---|---|
| Contract 3 — schema_registry.json format | `backend/schema_loader.py` read key `"joins"` but `schema_registry.json` uses key `"allowed_joins"`. The allowed-joins section of the schema digest sent to the LLM was silently empty. | Phase 3 chat: the LLM system prompt would have omitted allowed join information, increasing the risk of the LLM generating invalid SQL that references unallowed joins. No runtime crash — just a silent degradation in AI quality. | Changed `registry.get("joins", [])` to `registry.get("allowed_joins", [])` in `backend/schema_loader.py`. Also improved the join formatting to expand each join object into a readable string rather than printing the raw dict. |

---

## Silent misalignments (no merge conflict, but runtime failure)

| File | What one side assumed | What the other side built | Risk if not fixed |
|---|---|---|---|
| `backend/schema_loader.py` vs `data/schema_registry.json` | Naveen assumed the join array key would be `"joins"` | Pathey used `"allowed_joins"` to match the integration contract literally | LLM schema digest silently omits join info — no crash, but AI generates lower-quality SQL without join guidance |
| `backend/config.py` DB_PATH vs `data/load_who.py` | Backend assumes the server is always run from repo root (`"data/who_health.duckdb"` is a relative path resolved at runtime) | `load_who.py` uses `os.path.dirname(__file__)` to write the DB — always an absolute path | If `uvicorn` is ever run from a directory other than repo root (e.g., `cd backend && uvicorn main:app`), the backend cannot find the database. This is a latent CWD dependency, not caught by any test or error at write time. |
| `backend/config.py` vs runtime environment | `ANTHROPIC_API_KEY` was declared as a required field with no default. Pydantic validates this at import time. | Key is only needed for Phase 3 chat — `GET /charts` never calls the Claude API | Backend crashes at startup with a Pydantic validation error if `.env` is missing or the key is absent. Fixed by defaulting to `""`. On hackathon day, distribute `.env` files before anyone boots the backend. |
| `dashboard/app.py` import paths vs Python path | All dashboard imports use `from dashboard.xxx import ...` — requires `dashboard` to be a package on `sys.path` | Running `streamlit run dashboard/app.py` directly does not add repo root to `sys.path` | `ModuleNotFoundError: No module named 'dashboard'` on every cold start. Fixed by always prefixing with `PYTHONPATH=.`. Baked into Makefile — use `make backend` and `make dashboard`, never bare `uvicorn`/`streamlit` commands. |

---

## Assumption mismatches per person

### Pathey assumed...
- The backend would read `"allowed_joins"` from the registry (correct per the written contract, but Naveen's code used `"joins"`).
- The `sex` column filter (`BTSX`) was documented in the registry and would be used by backend SQL. Backend did use it — this assumption held.
- The backend would run from repo root and resolve `data/schema_registry.json` as a relative path. This holds as long as the startup convention is followed.

### Naveen assumed...
- The schema registry used a `"joins"` key (not `"allowed_joins"`). This was the one incorrect assumption — the registry and the integration contract both say `"allowed_joins"`.
- The DB would always be reachable at `data/who_health.duckdb` relative to CWD. No absolute-path guard was added. Correct in practice but fragile if startup convention is broken.
- `make_chart_spec` columns (`country_name`, `value`) in the SQL SELECT aliases would match what the dashboard reads via `x_key`/`y_key`. This held — Pathey's schema matched.

### Marco assumed...
- The backend would return `chart_type` as one of `"bar"`, `"line"`, `"area"` — and built rendering logic only for those three (with a fallback to bar for others). Naveen's static charts all use `"bar"`. This is fine for Phase 1, but an unwritten constraint that would break if someone added a `"scatter"` chart ID without telling Marco.
- The `data` field in each chart object would be a non-null list. Naveen guaranteed this through Pydantic (`list[dict]`). The assumption held.
- `selected_chart_id` would be a raw string matching a key in `LOWER_IS_BETTER_CHARTS`. This is correct — no transformation occurs between the backend chart_id and the set membership check.
- The backend would handle `chart_id: null` gracefully in POST /chat. Naveen's stub accepts it as `chart_id: str | None = None`. Correct.

---

## What to pre-agree before the real hackathon

Ordered by risk (most dangerous first):

1. **All cross-boundary key names in plain text, before anyone writes code** — The `"joins"` vs `"allowed_joins"` mismatch would have been a 5-second verbal conversation but cost integration time and nearly degraded AI quality silently. Write key names in `INTEGRATION_CONTRACTS.md` first and both parties read it before coding.

2. **DB path convention — absolute vs relative, and which directory to run from** — Both the data pipeline and the backend must agree on a single canonical DB path. The safest choice is to have the backend accept an environment variable for the DB path and document in `HACKATHON_SETUP.md` that servers must be started from repo root. Pre-agree this convention before the data person writes the ingestion script.

3. **The set of chart types the dashboard will render** — Marco built logic for `bar`, `line`, `area` only. If Naveen adds a new chart with `chart_type = "scatter"`, it silently falls back to bar. Pre-agree the full list of chart types and what the fallback behavior is, and lock it in the integration contract.

4. **Column aliases produced by SQL must be written into the contract, not inferred** — The backend SQL uses `c.country_name` and `cd.value` and the dashboard reads them via `x_key`/`y_key`. This worked because both sides happened to use the same names. In a real hackathon with different people, explicitly write the expected `x_key` and `y_key` values into Contract 1.

5. **CWD startup convention for every process** — Both `backend/config.py` (relative DB path) and `data/load_who.py` (dirname-of-file absolute path) depend implicitly on the caller running from repo root. Always use `make backend` / `make dashboard` — never bare `uvicorn` or `streamlit` commands, as these don't set `PYTHONPATH=.` and don't guarantee CWD.

6. **Schema registry file must be committed (or pre-populated) before backend coding starts** — `backend/schema_loader.py` raises `FileNotFoundError` at startup if the file is missing. On hackathon day, if Pathey is still building the ingestion pipeline when Naveen tries to start the backend, nothing will boot. Pre-agree that a stub `schema_registry.json` is committed to the repo before the parallel coding sprint begins.

7. **Chat endpoint stub vs live** — Naveen's POST /chat returns a hardcoded stub string. Marco's chat panel displays it without error. This works for demo purposes but the integration contract should say explicitly "Phase 3 — chat is a stub in this sprint" so Marco does not build UI that depends on real AI responses being present.

---

## Recommended day-of sequence

Based on this simulation, the safest order to unblock everyone:

1. **Pathey first: commit `data/schema_registry.json` with all table/column/join definitions** — unblocks Naveen's backend startup and all SQL validation logic. This is the single dependency that blocks the most work.
2. **Naveen second: verify `data/schema_registry.json` exists and boot the backend** — once `GET /charts` returns a valid response, Marco can run the dashboard end-to-end.
3. **Marco can start UI scaffolding in parallel with steps 1-2** using the hardcoded fallback charts (empty `data: []` graceful state) — the dashboard does not crash when the backend is absent.
4. **Data ingestion last: Pathey runs `data/load_who.py` to populate the DuckDB file** — this is independent of all UI and backend structure work and can be done any time after the schema is committed.
5. **Integration smoke test together**: all three run `uvicorn backend.main:app --reload` from repo root, then `streamlit run dashboard/app.py`. Verify all 6 charts render with real data.

---

## Integration checklist for real hackathon day

- [ ] `data/schema_registry.json` committed to repo before parallel sprint begins
- [ ] All JSON key names verified match between producer and consumer (especially `"allowed_joins"` vs any assumed alias)
- [ ] Everyone uses `make backend` / `make dashboard` — never bare `uvicorn` / `streamlit` (PYTHONPATH + CWD)
- [ ] `.env` file with `ANTHROPIC_API_KEY` distributed to Naveen's machine before backend starts
- [ ] `INTEGRATION_CONTRACTS.md` updated with exact SQL column aliases for `x_key` and `y_key` per chart
- [ ] Chart types supported by dashboard listed explicitly in the contract
- [ ] `make test` passing on every machine before parallel sprint begins (103 tests, <1s)
- [ ] Backend `GET /charts` smoke-tested (`curl http://localhost:8000/charts`) before Marco starts live API calls
- [ ] Chat endpoint stub status agreed — everyone knows it returns a placeholder until Phase 3
- [ ] DuckDB file created by running `make load` from repo root, confirmed before demo
- [ ] `make test-ui` passing after integration merge (Playwright confirms 6 charts render)
- [ ] Each person confirms: "I have read `INTEGRATION_CONTRACTS.md` and my code matches it"
