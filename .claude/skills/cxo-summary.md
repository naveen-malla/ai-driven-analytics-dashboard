---
name: cxo-summary
description: Generate a boardroom-ready executive summary from a set of dashboard chart insights. Takes multiple chart titles and data points, returns a polished 200-word CXO summary with headline, bullets, and a recommended action.
---

You are writing for hospital C-suite executives: CEO, CFO, CMO, COO.

Given a set of chart titles and their key data insights:

## Output structure

**Headline** (2 sentences max)
A concise statement of the most important finding across all charts. Lead with the insight, not the method.

**Key findings** (3–5 bullets)
- One finding per bullet
- Each bullet must include at least one specific number
- Lead with the implication, not the description
- Example: "Only 9% of hospitals achieve a 5-star CMS rating — most fall in the 2–3 star range, indicating significant quality headroom"

**Recommended next action** (1–2 sentences)
What should a CXO do with this information? Be specific. Reference the data.

## Tone rules

- Confident and direct — no hedging language like "it appears" or "it might be"
- Data-driven — every claim needs a number
- No jargon — no mention of SQL, DuckDB, CMS measure IDs, or column names
- No caveats about data quality unless they materially affect the finding (in that case, state it plainly)
- Total length: 150–250 words

## Data integrity rules

- If a metric includes "Not Available" hospitals in the majority, flag this plainly: "Note: X% of hospitals did not report this metric."
- Never present "Not Available" as a negative performance indicator
- Never infer causation from descriptive data — say "associated with" not "caused by"

## Example output

**National hospital quality is concentrated in the middle — with room to lead**

Across 4,700 CMS-rated US hospitals, only 450 (9.6%) achieved a 5-star quality rating, while 37% remain at 3 stars or below. Hospitals in the Midwest show consistently higher readmission rates for heart failure than the national average, and patient satisfaction scores closely track overall quality ratings.

- 9.6% of hospitals hold a 5-star CMS rating; 450 facilities set the benchmark for quality leadership
- Heart failure 30-day readmission rates in the South average 22.8% — 1.4 points above the national rate of 21.4%
- Hospitals rated 4–5 stars score 0.8 points higher on HCAHPS patient satisfaction than 1–2 star hospitals
- 18% of hospitals did not report sufficient data for an overall rating — a potential benchmark gap

**Recommended action**: Prioritize HCAHPS improvement initiatives at facilities currently rated 2–3 stars — patient experience is both a CMS rating driver and a leading indicator of loyalty and referrals.
