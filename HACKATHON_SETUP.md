# Hackathon Day-Of Setup

**Time budget**: 30 minutes to be fully operational.
**Project**: Kasha Unified Insights Platform
**Hackathon date**: Week of 2026-04-06 — 6 hours, 3 people

---

## 0. Prerequisites — confirm BEFORE hackathon day

Do not arrive with anything in this table missing. Debugging installs during the 6-hour window wastes the whole team.

### Accounts & access (Naveen sets up in advance)
- [ ] GitHub repo created — all three (Naveen, Marco, Pathey) added as collaborators with **write access**
- [ ] Anthropic API key — each person has their own, or use a shared key from a password manager (1Password / Bitwarden). **Do not share in Slack or email.**
- [ ] Kasha database credentials — Pathey confirms access to the relevant internal DBs before hackathon day

### Software (each person installs on their own machine)

| Tool | Mac install | Windows install | Verify |
|------|------------|-----------------|--------|
| Git | pre-installed or `brew install git` | [git-scm.com](https://git-scm.com) | `git --version` |
| Python 3.12+ | `brew install python@3.12` | [python.org](https://python.org) — use the installer | `python3 --version` |
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` | `uv --version` |
| VS Code | [code.visualstudio.com](https://code.visualstudio.com) | same | `code --version` |
| Claude Code CLI | `npm install -g @anthropic-ai/claude-code` (requires Node 18+) | same | `claude --version` |
| Node 18+ (for Claude Code) | `brew install node` | [nodejs.org](https://nodejs.org) LTS installer | `node --version` |

### VS Code extensions (install via Extensions panel — Ctrl+Shift+X)
- **Claude Code** (Anthropic) — AI assistant in sidebar
- **Python** (Microsoft) — linting and IntelliSense
- **Pylance** (Microsoft) — type checking
- **GitLens** (GitKraken) — inline blame and history

### Windows-specific notes (Marco)
- Use **PowerShell**, not CMD, for all commands
- `python3` may be `python` on Windows — if a command fails, try the other
- If `git status` shows all files modified after cloning: run `git config core.autocrlf false` then `git checkout .`
- All Python code uses `pathlib.Path` — no hardcoded `/` vs `\` issues

---

## 1. Clone and install (5 min)

```bash
git clone https://github.com/<org>/kasha-insights-starter
cd kasha-insights-starter

# Create virtual environment and activate
uv venv
source .venv/bin/activate          # Mac/Linux
.venv\Scripts\activate             # Windows PowerShell

# Install all dependencies
uv pip install -r backend/requirements.txt
uv pip install -r dashboard/requirements.txt
```

Confirm everything installed:
```bash
python3 -c "import fastapi, duckdb, anthropic, streamlit, plotly; print('OK')"
```
Should print `OK`. If any import fails, run `uv pip install <package-name>`.

**What gets installed** (FYI — no manual installs needed):
- `fastapi`, `uvicorn` — backend API server
- `duckdb` — in-process analytics database (no server setup)
- `anthropic` — Claude API SDK
- `pydantic` — data validation
- `streamlit`, `plotly`, `httpx` — dashboard UI and HTTP client

---

## 2. Configure environment (2 min)

```bash
cp .env.example .env
```

Open `.env` and fill in:

```
ANTHROPIC_API_KEY=sk-ant-...          # Required — from anthropic.com/api
DATABASE_PATH=data/kasha.duckdb       # Pathey updates this once DB is ready
SCHEMA_REGISTRY=data/schema_registry.json
```

`.env` is in `.gitignore` — it will never be committed. Do not share its contents in chat.

---

## 3. Create your git branch (1 min)

Each person works on their own named branch. **Do not push directly to `main`.**

```bash
# Naveen
git checkout -b naveen/backend

# Pathey
git checkout -b pathey/data

# Marco
git checkout -b marco/dashboard
```

---

## 4. Load data — Pathey does this first (10 min)

**Everyone waits for Pathey to finish this step before writing any SQL.**

```bash
# Pathey only
python3 data/load_kasha.py
```

After loading, verify the database is accessible:
```bash
python3 -c "
import duckdb
con = duckdb.connect('data/kasha.duckdb', read_only=True)
print(con.execute('SHOW TABLES').fetchall())
"
```

Pathey then opens `data/schema_registry.json` and fills in the real column names and table definitions. **Post in Slack when done** — Naveen and Marco unblock immediately.

**Fallback**: If Kasha DB is unavailable, use the CMS demo database:
```bash
DATABASE_PATH=data/cms_hospital.duckdb  # update .env
```

---

## 5. Run the stack (5 min)

Open **two terminals** (both with `.venv` activated).

**Terminal 1 — Backend**:
```bash
uvicorn backend.main:app --reload --port 8000
```
Confirm: `curl http://localhost:8000/charts` returns a JSON array (even if empty).

**Terminal 2 — Dashboard**:
```bash
streamlit run dashboard/app.py
```
Confirm: Browser opens at `http://localhost:8501` with no Python traceback.

---

## 6. Confirm Claude Code is working (2 min)

Open Claude Code (sidebar in VS Code or `claude` in terminal). Run:

```
/schema-check Is the database connected and the schema loaded?
```

If it reads `data/schema_registry.json` and reports table names, you are ready to build.

---

## 7. Who does what in the first 30 minutes

| Person | First 30-min task | What it unblocks |
|--------|-------------------|-----------------|
| **Pathey** | Connect Kasha data, run `load_kasha.py`, populate `schema_registry.json` | Everyone — no SQL possible without the schema |
| **Naveen** | Create `backend/config.py`, `backend/database.py`, confirm `GET /charts` returns 200 | Marco — dashboard needs a live API to call |
| **Marco** | Run `/ui-ux-pro-max plan` to pick theme, create `.streamlit/config.toml` and `dashboard/theme.py` | No dependencies — can start immediately |

After 30 minutes: **5-minute sync**. Pathey shares final schema column names. Naveen confirms API is live. Marco shares theme palette. Then async coding starts.

---

## 8. Sync schedule

| Time | Duration | What happens |
|------|----------|-------------|
| Hour 0 | 5 min | Everyone confirms setup done, Pathey has schema |
| Hour 1 | 5 min | Pathey shares final `schema_registry.json` — Naveen loads it into schema_loader |
| Hour 4 | 15 min | **Integration checkpoint** — wire dashboard ↔ API ↔ DB end-to-end |
| Hour 5.5 | 15 min | Demo dry run — run `/demo-review`, fix any FAIL items |
| Hour 6 | Demo | 5-minute live demo |

---

## 9. Integration checklist (hour 4 sync)

Before merging branches at hour 4:

- [ ] `GET /charts` returns all static charts with correct `chart_id` keys
- [ ] `dashboard/api_client.py` calls `/charts` and renders at least one chart without error
- [ ] `POST /chat` with a valid question returns a non-empty response
- [ ] `POST /chat` with "What is the staffing cost per bed?" returns a rejection message
- [ ] `data/provenance.json` has at least one entry
- [ ] No hardcoded CMS or column-name references in any user-facing string

Merge order: `pathey/data` → `naveen/backend` → `marco/dashboard`

If a merge conflict happens: **Naveen resolves** (owns the integration layer).

---

## 10. Emergency fallbacks

| Problem | Fix |
|---------|-----|
| Kasha DB unavailable | Switch `DATABASE_PATH` to `data/cms_hospital.duckdb` in `.env` |
| Claude API rate limit | Add `time.sleep(1)` between requests, reduce concurrent calls to 1 |
| `python3` not found on Windows | Try `python` instead; add Python to PATH if neither works |
| Streamlit won't start | Check for import errors in `dashboard/app.py` — run `python3 dashboard/app.py` to see the traceback |
| Schema mismatch after Pathey updates | Pathey updates `schema_registry.json`, Naveen restarts `uvicorn` |
| Git shows all files modified (Windows) | `git config core.autocrlf false` then `git checkout .` |

---

*Run `/hackathon-brief` inside Claude Code for a current-state summary at any point.*
*Run `/demo-review` before presenting to verify nothing is broken.*
