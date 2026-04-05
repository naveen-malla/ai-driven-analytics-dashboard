# Marco — Product Manager & UX Lead

## Role
Product owner and design decision-maker. Marco defines *what* the CXO sees and *why* — not how the code works. He does not write Python from scratch. His AI (Claude Code) helps him produce all code, which must be simple enough for him to read, understand, and later edit.

## What you own (hackathon day)
- `dashboard/` — all Streamlit UI files
- `.streamlit/` — Streamlit theme config

## What you DO NOT own or touch
- `backend/` — Naveen owns this
- `data/` — Pathey owns this
- `.claude/` — Naveen owns this

## Your expertise
- Product strategy and CXO communication
- Information hierarchy and visual design decisions
- What health-sector executives actually need to see
- Streamlit (can read and edit simple Python, cannot write complex logic)
- Design thinking, wireframing, narrative structure

## NOT your expertise
- FastAPI, DuckDB, SQL, backend architecture
- Complex Python patterns (list comprehensions, decorators, async)
- Database schemas or API internals

## What you know about the other workstreams
- Naveen's backend serves `GET http://localhost:8000/charts` returning chart data
- The response shape is in `.github/INTEGRATION_CONTRACTS.md` (Contract 1) — exactly what `dashboard/api_client.py` consumes
- The 6 chart IDs are in Contract 2 — dashboard must render all 6 by these IDs
- `POST /chat` is in Contract 4 — dashboard calls this for the AI chat panel

## What you don't know (and don't need to)
- How the backend processes SQL
- What the DuckDB schema looks like
- How the Claude API works

## How you work
- Start with the design system — run ui-ux-pro-max to pick theme, colors, typography
- Write a design brief in `dashboard/DESIGN_BRIEF.md` before touching any code
- All Python code must be readable by a non-programmer — no clever patterns, every line commented
- Variable names are spelled out fully: `chart_data` not `d`, `country_name` not `cn`
- Use `st.` Streamlit functions directly — no custom abstractions that are hard to follow
- If in doubt between two design choices, pick the one that makes the CXO's key insight easier to see

## Design principles (non-negotiable)
- The dashboard tells a story — it's not a data dump
- Every chart answers one executive question
- The most important insight is visible without scrolling
- The AI chat panel is secondary — static charts are primary for a demo

## Day-of priority order
1. `.streamlit/config.toml` + `dashboard/theme.py` — establish visual identity immediately
2. `dashboard/DESIGN_BRIEF.md` — write the product spec so Naveen knows what to wire up
3. `dashboard/app.py` skeleton — layout structure, even with placeholder chart slots
4. Wire up `api_client.py` → real chart data

## First 30-minute task (hackathon day)
Run ui-ux-pro-max design system. Create `.streamlit/config.toml` and `dashboard/theme.py`.
Start `dashboard/DESIGN_BRIEF.md` with the CXO narrative and chart ordering rationale.
These can be done before Pathey's data pipeline is ready.
