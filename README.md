# AI-Driven Healthcare Analytics Dashboard

A CXO-facing healthcare analytics dashboard with a governed AI chat copilot, built using the full Claude ecosystem.

## What it does

- **Static dashboard**: 6 executive charts derived from CMS Hospital Compare public data
- **Chart follow-up**: ask the AI about any chart — it explains or modifies it using the chart's SQL and data provenance
- **New analysis**: ask a new question; the AI checks if it can be answered from the available schema, generates SQL, validates it, runs it, and renders a chart
- **Rejection**: questions outside the available data scope are rejected with a clear reason

## Tech stack

| Layer | Technology |
|-------|-----------|
| Dashboard UI | Streamlit + Plotly |
| Backend API | FastAPI + Python 3.12 |
| Database | DuckDB (read-only, CMS CSV data) |
| AI runtime | Claude API (`claude-sonnet-4-6`) |
| Dev tooling | Claude Code (subscription) |

## Dataset

CMS Hospital Compare public data — fully public, no PHI.

- ~5,000 hospitals across the US
- Metrics: overall quality ratings, readmission rates, patient satisfaction (HCAHPS), complications, timely care
- Source: [data.cms.gov/provider-data/topics/hospitals](https://data.cms.gov/provider-data/topics/hospitals)

## Setup

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Anthropic API key

### 1. Clone and install
```bash
git clone https://github.com/naveen-malla/ai-driven-analytics-dashboard
cd ai-driven-analytics-dashboard
uv venv && source .venv/bin/activate
uv pip install -r backend/requirements.txt
uv pip install -r dashboard/requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Download and load data
```bash
# Download CMS CSVs (see data/README.md for download links)
python data/load_cms.py
```

### 4. Run the app
```bash
# Terminal 1 — Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Dashboard
streamlit run dashboard/app.py
```

Open [http://localhost:8501](http://localhost:8501)

## Claude ecosystem features used

| Feature | Location | Purpose |
|---------|----------|---------|
| Project memory | `CLAUDE.md` | Dataset schema, metric definitions, coding rules |
| Subagents | `.claude/agents/` | `data-analyst`, `sql-validator` |
| Skills | `.claude/skills/` | `/explain-chart`, `/new-chart`, `/schema-check`, `/cxo-summary` |
| Hooks | `.claude/settings.json` | PreToolUse: validate SQL; PostToolUse: save provenance |
| Tool calling | `backend/chat_orchestrator.py` | `execute_sql`, `render_chart` tools |
| Structured outputs | `backend/intent_classifier.py` | Pydantic `IntentResult` classification |
| Prompt caching | `backend/schema_loader.py` | Schema digest cached across requests |
| Streaming | `backend/handlers/new_analysis.py` | Long analysis streamed to UI |

## Project structure

```
.
├── CLAUDE.md               ← Project memory (Claude Code reads this)
├── .claude/                ← Agents, skills, hooks config
├── backend/                ← FastAPI app + Claude API integration
├── dashboard/              ← Streamlit UI
├── data/                   ← Schema registry, provenance, load script
└── .github/                ← PLAN.md, DECISIONS.md, NOTES.md
```

## Demo script (5 minutes)

1. Show the static dashboard — 6 charts, explain the dataset context
2. Click "Ask about this chart" on the star rating distribution → ask "What does a 3-star rating mean?"
3. Ask a new question: "Which states have the highest readmission rates for heart failure?"
4. Show a rejection: "What is the average cost per hospital bed?"
5. Show the generated chart with its SQL provenance

## Architecture decisions

See [.github/DECISIONS.md](.github/DECISIONS.md)
