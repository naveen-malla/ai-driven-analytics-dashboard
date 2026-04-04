---
name: to-showcase
description: Converts this project from hackathon-prep framing to a clean showcase project. Rewrites README.md, CLAUDE.md, and .github/ docs to present the work as a finished, portfolio-ready product — removing internal prep language, replacing personal context with professional framing, and highlighting the Claude ecosystem features demonstrated.
---

This project was built as hackathon preparation. You are now converting it into a showcase — something that can be shared publicly, shown to Marco at the hackathon, or used as a portfolio piece that demonstrates production-quality use of the Claude ecosystem.

## Step 1 — Read current state

Read these files before making any changes:
1. `README.md` — current public-facing description
2. `CLAUDE.md` — project memory (contains prep/hackathon framing)
3. `.github/PLAN.md` — build plan
4. `.github/DECISIONS.md` — architecture decisions
5. `.github/NOTES.md` — working notes

## Step 2 — Identify prep language to replace

Scan all five files for language that:
- Refers to this as a "rehearsal", "prep", or "practice" project
- References the hackathon as a future goal (it is now complete)
- Uses first-person internal voice ("I want to learn...", "my manager Marco...")
- Mentions "Caccia" (old company name — correct to "Kasha" if found)
- Contains TODO-style notes or "populate later" placeholders that were never filled in

List every instance before making any changes.

## Step 3 — Rewrite README.md as a showcase document

The README is the first thing anyone sees. Rewrite it to:

**Lead with what the project demonstrates, not how it was built:**
- Open with a 2-sentence description: what the dashboard does, who it is for, what dataset it uses
- Follow with a "Claude ecosystem features" section that names each feature concisely: Claude Code skills, agents, hooks, Claude API tool calling, structured outputs, prompt caching, streaming — and what each one does in this project
- Do NOT mention "hackathon prep", "rehearsal", or "learning exercise" anywhere

**Replace internal framing with professional framing:**
- Before: "Built to learn the Claude ecosystem before a hackathon"
- After: "Demonstrates a production-grade governed analytics copilot pattern using the Claude ecosystem"

**Keep these sections** (they are already good):
- Architecture diagram / layers table
- Setup instructions
- Demo script
- Link to DECISIONS.md

**Remove or rewrite these:**
- Any section that reads as a personal journal or status update
- References to what "will be built" — replace with what was built

## Step 4 — Rewrite CLAUDE.md Hackathon Context section

The Hackathon Context section was written for internal use. For the showcase version:
- Replace the section title `## Hackathon Context` with `## Project Origin`
- Reframe: "This project was built as a full-stack proof of concept demonstrating the governed analytics copilot pattern. The same architecture is being applied at [Kasha](kasha.co) for a CXO insights platform over internal distribution and health access data."
- Remove the team roles table (it was for internal coordination)
- Remove the "what will be stripped" list — it served its purpose and is no longer relevant
- Keep: the Kasha context (it shows real-world applicability)

## Step 5 — Clean up .github/ docs

**PLAN.md**:
- Replace the "Current objective" line with a one-liner: "Complete — see DECISIONS.md for architecture rationale."
- Mark all Phase 0–5 items as `[x]` if they are done (check the actual files on disk before marking)
- Keep Phase 6 but retitle it: `Phase 6 — Kasha Adaptation` (remove "Hackathon Prep" framing)
- Remove any items that reference personal learning goals

**DECISIONS.md**: No changes needed — it is already written in professional, permanent voice.

**NOTES.md**:
- Remove any section that is still an empty placeholder ("Populate during Phase X")
- Condense populated sections into clean findings
- Remove personal notes or todo comments

## Step 6 — Update .claude/skills/ descriptions

Scan the frontmatter `description` field of each skill file in `.claude/skills/`. Update any description that mentions "prep", "hackathon", or is written for an internal audience. The description is shown in the Claude skills list — it should read like a professional tool description, not an internal note.

Specifically update:
- `hackathon-brief.md` → rename to `project-brief.md` and update description to: "Reads current project state from disk and outputs a structured brief — what has been built, key decisions, open questions, and suggested next steps."
- `demo-review.md` → description is already professional, no change needed

## Step 7 — Final review

After all rewrites, verify:
- [ ] No "rehearsal", "prep", "learning exercise", or "practice" language remains in any user-facing file
- [ ] README reads as a complete, finished project — not a work in progress
- [ ] CLAUDE.md Hackathon Context → Project Origin is coherent and professional
- [ ] All placeholder text ("Populate during Phase X", "[REPLACE WITH KASHA]") is either filled in or removed
- [ ] The Claude ecosystem features table in README accurately reflects what was actually built
- [ ] PLAN.md reads as a retrospective record, not a future roadmap

## Output

After completing all changes, output a summary:

```
SHOWCASE CONVERSION SUMMARY
============================
Files updated: [list]
Prep language removed: [count] instances
Placeholder text resolved: [count] instances
Skills renamed: [list]

SHOWCASE READY: [YES / NO]
If NO: [list remaining items]
```
