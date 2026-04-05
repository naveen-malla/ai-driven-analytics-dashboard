---
name: hackathon-brief
description: Reads current project state from disk and outputs a 2-minute team brief — what has been built, what is pending, locked decisions, open questions, and suggested next 2 hours. Run when Marco or Pathey joins and needs to get up to speed fast.
---

Read the current project state from files before writing anything. Do not use memory or assumptions — check the actual files on disk.

## Step 1 — Read these files in order

1. `CLAUDE.md` — architecture, stack, team roles, hackathon context
2. `.github/PLAN.md` — which tasks are `[x]` (done) vs `[ ]` (pending)
3. `.github/DECISIONS.md` — locked architecture decisions
4. `.github/NOTES.md` — populated findings (skip any section still labelled "Populate during Phase X")
5. `backend/` — list the files that actually exist right now
6. `dashboard/` — list the files that actually exist right now
7. `data/` — list the files that actually exist right now

## Step 2 — Output the brief

Format exactly as below. Keep it tight — readable in 2 minutes.

---

### Hackathon Brief — [today's date]

**What this is**: Rehearsal project for the Kasha Unified Insights Platform hackathon (week of 2026-04-06). Architecture proven on WHO GHO public data before rebuilding on Kasha's actual databases. Team: Naveen (backend/AI), Pathey (data), Marco (UI/UX).

---

**What has been built** (files actually on disk right now):

- *Backend*: [list backend/ files, or "not started"]
- *Dashboard*: [list dashboard/ files, or "not started"]
- *Data*: [list data/ files, or "not started"]
- *Claude ecosystem*: [list .claude/agents/ and .claude/skills/ files]

---

**What is pending** (next 5–8 unchecked items from PLAN.md, grouped by phase):

[list — most recent incomplete phase first]

---

**Locked decisions** (from DECISIONS.md — do not re-debate these):

[one-liner per decision: "Topic: what was decided"]

---

**Open questions** (genuine unknowns — verify against NOTES.md before listing):

List 3–5 questions that are actually unresolved right now. Only include questions where the answer has not already been documented in NOTES.md or DECISIONS.md.

---

**Your role on hackathon day**:

- **Marco** → Own `dashboard/` and `.streamlit/`. First task: run `/ui-ux-pro-max plan` to pick theme, create `dashboard/theme.py` and `.streamlit/config.toml`. No backend dependency needed to start.
- **Pathey** → Own `data/`. First task: connect Kasha databases, run `load_who.py` as reference then the Kasha equivalent, populate `schema_registry.json` with real column names. Everyone waits on you before writing SQL.
- **Naveen** → Own `backend/` and `.claude/`. Current phase priority: [read from PLAN.md — the first incomplete phase].

---

**Suggested next 2 hours** (from PLAN.md pending items — list items that unblock others first):

1. [Person] — [specific action, file to create or command to run] — unblocks [who]
2. [Person] — [action]
3. [Person] — [action]
4. [Person] — [action]

---

*Re-run `/hackathon-brief` at any time to get a fresh current-state view.*
*Run `/demo-review` before any demo to verify nothing is broken.*
