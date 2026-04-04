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

Write a 3–5 sentence explanation suitable for a C-suite hospital executive (CEO, CFO, CMO, COO).

## Structure your response as:

**[Chart Title]**

[1 sentence: what this chart shows and what the metric means in plain English]

[1-2 sentences: what stands out or is notable in the current data — use specific numbers]

[1 sentence: what this means for hospital operations or patient care]

[Optional: 1 sentence call to action if the data suggests a specific next step]

## Tone rules

- Plain English — no SQL jargon, no mention of table names or column names
- Data-driven — always reference at least one specific number from the data
- Honest — if a metric is "Not Available" for many hospitals, say so rather than skipping it
- Concise — 3–5 sentences maximum, no bullet points

## Example

**Hospital Overall Rating Distribution**

This chart shows how CMS assigns each hospital a quality star rating from 1 (lowest) to 5 (highest), based on a composite of mortality, safety, readmission, patient experience, and timely care measures. Nationally, the largest group of hospitals — about 1,200 — falls at the 3-star level, with only 450 hospitals achieving a top 5-star rating. Fewer than 300 hospitals hold a 1-star rating, suggesting most facilities meet at least a baseline national standard. Hospitals below 3 stars may want to investigate their weakest contributing measures to identify targeted improvement opportunities.
