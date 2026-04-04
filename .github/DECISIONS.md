# Architecture Decisions

Locked decisions for this project. Do not reverse without updating this file.

---

## 2026-04-04 — Governed analytics copilot pattern

**Decision**: The AI operates as a governed copilot inside a controlled system, not a free-form code-writing agent.

**Constraints**: The AI may only run pre-validated SQL via the `execute_sql` tool. It cannot write arbitrary Python, access the filesystem, or run shell commands. All SQL passes through `sql_validator.py` before execution.

**Why**: CXO audience requires trustworthy, explainable outputs. "The AI wrote a script" is not auditable. SQL + chart spec is reviewable and reproducible.

---

## 2026-04-04 — Read-only data access only

**Decision**: The DuckDB database is opened in read-only mode. No writes, no schema changes, no inserts.

**Why**: Public dataset that doesn't change during a demo. Prevents accidental corruption. Simplifies security model — no credentials needed, no access control.

---

## 2026-04-04 — Frontend: Streamlit + Plotly (not Next.js)

**Decision**: Python-only stack for the UI. Streamlit for layout/interaction, Plotly for charts.

**Why**: Weekend build timeline. Python-only means no context switching between JS and Python. Streamlit is fast to iterate on. The CXO demo needs functional, not pixel-perfect.

**Trade-off**: Less visual polish than Next.js + Tailwind + shadcn/ui. Accepted for this learning project.

---

## 2026-04-04 — Claude API model: claude-sonnet-4-6

**Decision**: `claude-sonnet-4-6` for all app runtime calls (intent classification, tool calling, analysis).

**Why**: Best balance of capability and cost for this use case. Structured outputs and tool calling work reliably on Sonnet. Opus is available for complex analysis if needed but not the default.

---

## 2026-04-04 — Database: DuckDB over Postgres

**Decision**: DuckDB in-process, reading CMS CSVs directly (no Postgres server).

**Why**: No server setup required. DuckDB directly queries CSV/Parquet. Perfect for a weekend build and a read-only analytics use case. Can be swapped for Postgres later with minimal changes to `database.py`.

---

## 2026-04-04 — Chart provenance as first-class artifact

**Decision**: Every chart (static and AI-generated) has a provenance record in `data/provenance.json` containing its SQL, data snapshot, chart spec, and metric definition.

**Why**: Chart follow-up mode depends entirely on provenance. Without it, the AI has to re-derive context from scratch. Provenance makes follow-up deterministic and fast.

---

## 2026-04-04 — Intent classification before tool calling

**Decision**: Every chat request goes through `intent_classifier.py` first, which classifies into `explain_chart | modify_chart | new_analysis | reject` before any tools are called.

**Why**: Prevents tool misuse. The classifier can reject out-of-scope questions cheaply (no SQL executed, no DB hit) before any expensive downstream operations.

---

## 2026-04-04 — Prompt caching for schema digest

**Decision**: The schema digest (table/column descriptions from `schema_registry.json`) is placed in the system prompt with `cache_control: ephemeral` on every Claude API call.

**Why**: The schema block is ~2,000 tokens and repeated on every request. Caching it saves significant cost and reduces latency on the second+ call within the same session.

---

## 2026-04-04 — Dataset: CMS Hospital Compare

**Decision**: Use CMS Hospital Compare public data (data.cms.gov) as the primary dataset.

**Why**: Public (no PHI, no licensing issues). Healthcare-relevant for the CXO audience. Covers meaningful executive metrics: quality ratings, readmissions, patient satisfaction, complications. Structured, joinable CSVs with a clear schema.
