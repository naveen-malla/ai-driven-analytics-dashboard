---
name: explain-chart
description: Explain an existing dashboard chart in plain English to a CXO. Given a chart's provenance (SQL, data snapshot, metric definition, chart spec), produce a 3-5 sentence executive summary with key insight and context.
---

You have been given the provenance of a specific dashboard chart:
- **Chart title** and **metric definition**
- **SQL query** that generated it
- **Chart type** and axis keys
- **Data snapshot** (sample rows from last execution)

## Your task

Write a 3–5 sentence explanation suitable for a health-sector decision-maker (country health director, NGO programme lead, regional health coordinator, or health-tech CXO).

## Structure your response as:

**[Chart Title]**

[1 sentence: what this chart shows and what the metric means in plain English]

[1-2 sentences: what stands out or is notable in the current data — use specific numbers]

[1 sentence: what this means for hospital operations or patient care]

[Optional: 1 sentence call to action if the data suggests a specific next step]

## Tone rules

- Plain English — no SQL jargon, no mention of table names or column names
- Data-driven — always reference at least one specific number from the data
- Honest — if data is missing or NULL for a country, say so rather than skipping it
- Concise — 3–5 sentences maximum, no bullet points

## Example

**Contraceptive Prevalence Rate by Country**

This chart shows the percentage of women aged 15–49 currently using any contraceptive method (WHO indicator FP_CXUS_W_CURR), a key measure of reproductive health access across the region. Rwanda leads at approximately 64%, while Ethiopia sits at 41% — a 23-percentage-point gap that reflects significant variation in healthcare infrastructure and access across Kasha's core markets. Lower prevalence indicates higher unmet need for reproductive health products. Regions below 50% warrant targeted distribution investment to close the access gap.
