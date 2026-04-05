# Working Notes

Running notes and findings across the weekend build. Update as you discover things.

---

## WHO GHO Dataset Notes

*(Update after running data/load_who.py and inspecting the loaded data)*

### API structure
WHO GHO REST API endpoint: `https://ghoapi.azureedge.net/api/<INDICATOR_CODE>`
- Optional filter: `?$filter=SpatialDimType eq 'COUNTRY'` — returns country-level rows only
- Returns JSON with a `value` array; each element has: `IndicatorCode`, `SpatialDim` (country code), `TimeDim` (year), `NumericValue`, `Low`, `High`, `Dim1` (often sex: MLE/FMLE/BTSX)

### Column mapping (API → DuckDB table)
| API field | DuckDB column | Notes |
|-----------|--------------|-------|
| `SpatialDim` | `country_code` | ISO 3-letter code (RWA, KEN, etc.) |
| `TimeDim` | `year` | Integer |
| `NumericValue` | `value` | FLOAT — may be NULL |
| `Low` | `low_estimate` | FLOAT — confidence interval lower bound |
| `High` | `high_estimate` | FLOAT — confidence interval upper bound |
| `Dim1` | `sex` | "MLE", "FMLE", "BTSX" (both sexes) — use BTSX for most charts |

### Known data quality issues
- `value` is NULL for many country/year combinations — always filter `WHERE value IS NOT NULL`
- Some indicators only have data every 5 years (not annual) — check available years before building time series
- `sex = 'BTSX'` is "both sexes combined" — use this for summary charts unless a sex-disaggregated view is specifically requested
- Confidence intervals (`low_estimate`, `high_estimate`) are often NULL even when `value` is present — don't require them

### Target countries and codes
| Country | Code |
|---------|------|
| Rwanda | RWA |
| Kenya | KEN |
| Uganda | UGA |
| Ethiopia | ETH |
| Tanzania | TZA |

### Useful DuckDB queries for exploration
```sql
-- Check available years for a given indicator
SELECT indicator_code, year, COUNT(*) as country_count
FROM country_data
WHERE indicator_code = 'FP_CXUS_W_CURR'
GROUP BY 1, 2 ORDER BY 2;

-- Check which countries have data for all 6 indicators
SELECT country_code, COUNT(DISTINCT indicator_code) as indicators_present
FROM country_data WHERE value IS NOT NULL
GROUP BY 1 ORDER BY 2 DESC;

-- Preview latest value per country for an indicator
SELECT c.country_name, d.year, d.value
FROM country_data d JOIN countries c USING (country_code)
WHERE d.indicator_code = 'MDG_0000000025'
  AND d.sex = 'BTSX' AND d.value IS NOT NULL
ORDER BY d.year DESC LIMIT 10;
```

---

## FastAPI Notes

### Startup requirements (confirmed 2026-04-05)
- Must run from repo root with `PYTHONPATH=.` — use `make backend`, not bare `uvicorn`
- `ANTHROPIC_API_KEY` is optional at startup (defaults to `""`); only required when Phase 3 chat handler is live
- Database file `data/who_health.duckdb` must exist before first request to `GET /charts`; backend raises `FileNotFoundError` with a clear message if missing
- `data/schema_registry.json` must exist before `build_schema_digest()` is called (Phase 3); stub file is already committed so startup doesn't fail

---

## Claude API Notes

*(Populate during Phase 3)*

### Prompt caching verification
Check response for `cache_creation_input_tokens` on first call.
Check for `cache_read_input_tokens` on second call with same schema block.

### Tool calling loop pattern
```
call Claude → if stop_reason == "tool_use" → extract tool input → validate → execute → append tool_result → loop
             if stop_reason == "end_turn" → extract text → return
```

---

## Streamlit Notes

### Startup requirements (confirmed 2026-04-05)
- Must run with `PYTHONPATH=.` — use `make dashboard`, not bare `streamlit run`
- Running `streamlit run dashboard/app.py` without `PYTHONPATH=.` raises `ModuleNotFoundError: No module named 'dashboard'`
- Backend must be running on `:8000` for charts to load; app shows a warning instead of crashing when backend is absent

### Session state keys used
- `st.session_state.selected_chart_id` — currently selected chart for follow-up
- `st.session_state.chat_history` — list of {role, content, chart?} dicts

---

## Benchmark Question Results

*(Populate during Phase 5)*

| # | Question | Expected intent | Actual intent | Correct? | Notes |
|---|----------|----------------|---------------|----------|-------|
| 1 | | | | | |
