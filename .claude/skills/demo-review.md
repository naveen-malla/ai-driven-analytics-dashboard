---
name: demo-review
description: Pre-demo checklist — verifies SQL validator is active, all 6 static charts load, provenance.json is populated, out-of-scope rejection works, no internal jargon in UI, and chart accessibility basics pass. Run before every demo or presentation.
---

Run before every demo. Work through each check in order. Report PASS / FAIL / WARN for each item. Output a summary table at the end.

## Check 1 — SQL validator is active

Read `backend/sql_validator.py`. Confirm:
- File exists and is non-empty
- Contains all five validation checks: read-only (SELECT only), no multi-statement (no semicolons), known tables only, LIMIT present (≤500), no injection patterns
- `validate_sql()` is the sole entry point called by `backend/chat_orchestrator.py` — not bypassed anywhere

FAIL: "SQL validator not wired in — queries may reach DuckDB unvalidated."

## Check 2 — All 6 static charts defined

Read `backend/static_charts.py`. Confirm:
- Exactly 6 chart definitions present (or the count in CLAUDE.md if updated)
- Each has: `chart_id`, `title`, `sql`, `chart_type`, `x_key`, `y_key`, `metric_definition`
- No column names contain spaces (DuckDB normalizes to underscores — cross-check against `data/schema_registry.json`)

FAIL if fewer than 6. WARN if any column name looks wrong.

## Check 3 — provenance.json is populated

Read `data/provenance.json`. Confirm:
- File exists
- At least one entry per static chart (6 minimum)
- Each entry has: `chart_id`, `sql`, `data_snapshot` (non-empty array), `chart_spec`, `metric_definition`

FAIL if file missing. WARN for each `chart_id` with an empty `data_snapshot`.

## Check 4 — Out-of-scope rejection works

Read `backend/handlers/reject.py` and `backend/intent_classifier.py`. Confirm:
- `reject` intent exists in the classifier's output schema
- `reject.py` returns a user-facing message — no stack trace, no empty string
- Rejection message contains no SQL, DuckDB, column names, or internal system details

Trace these 3 questions through the classifier — all must route to `reject`:
1. "What is the average cost per hospital bed?"
2. "How many patients were admitted last year?"
3. "Why did readmission rates go up?"

FAIL for any question that would reach `new_analysis` or `explain_chart`.

## Check 5 — No internal jargon visible in UI

Read `dashboard/app.py` and all files in `dashboard/components/`. Search all user-facing strings (titles, labels, tooltips, placeholders, error messages) for:
- `indicator_code`, `country_code`, `SpatialDim`, `NumericValue`, `TimeDim`
- `DuckDB`, `schema_registry`, `ghoapi`
- Raw WHO indicator codes exposed directly (e.g. `FP_CXUS_W_CURR`) — these must be mapped to human-readable names

FAIL with exact file and line number for any match.

## Check 6 — Chart accessibility basics

Read `dashboard/components/chart_renderer.py` and `dashboard/theme.py`. Confirm:
- All Plotly charts have axis titles set — not raw column names like `x_key`
- Primary chart color is not mid-grey (`#808080` or similar) on a white background
- Charts have a title via Plotly layout title or `st.subheader`
- Any chart that uses color to distinguish categories has a legend or value labels

WARN for raw column names as axis labels. FAIL if no chart titles.

## Summary output

```
DEMO REVIEW SUMMARY
===================
Check 1 — SQL validator active:      [PASS|FAIL|WARN]
Check 2 — All 6 static charts:       [PASS|FAIL|WARN]
Check 3 — provenance.json populated: [PASS|FAIL|WARN]
Check 4 — Out-of-scope rejection:    [PASS|FAIL|WARN]
Check 5 — No internal jargon in UI:  [PASS|FAIL|WARN]
Check 6 — Chart accessibility:       [PASS|FAIL|WARN]

BLOCKERS (FAIL items): [list or "None"]
WARNINGS: [list or "None"]
DEMO READY: [YES / NO — fix all FAIL items before presenting]
```
