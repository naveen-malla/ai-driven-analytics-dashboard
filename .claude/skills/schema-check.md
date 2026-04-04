---
name: schema-check
description: Check if a natural language question can be answered from the available CMS Hospital Compare schema. Returns answerable/not-answerable/partial with exact table and column names, and explains what is missing if not answerable.
---

Read `data/schema_registry.json` first. Then, given a natural language question:

## Step 1 — Identify required data dimensions

What dimensions does this question need?
- A metric (what to measure)
- A grouping dimension (by state, by hospital type, by measure, etc.)
- A time dimension (CMS data is a snapshot — no time series unless explicitly stored)
- A filter (specific measure, hospital type, state, etc.)

## Step 2 — Map to available schema

For each required dimension, find the exact table and column name in the schema.

## Step 3 — Classify and respond

**Answerable** — all required dimensions exist:
```
ANSWERABLE
Tables: hospitals, readmissions
Key columns: hospitals.state, readmissions.score, readmissions.measure_id
Notes: score column is VARCHAR — needs CAST and NULL handling
```

**Not answerable** — required data is missing:
```
NOT ANSWERABLE
Missing: [describe what data would be needed]
Reason: CMS Hospital Compare does not include [cost / revenue / patient volume / diagnoses / staffing / etc.]
Available metrics that are related: [suggest what CAN be answered that is close]
```

**Partial** — some dimensions are available, others aren't:
```
PARTIAL
Answerable part: [what can be answered]
Missing part: [what cannot]
Suggested reformulation: [a question that CAN be answered from available data]
```

## Common not-answerable categories in this dataset

- **Financial**: cost per procedure, revenue, reimbursement rates, billing data
- **Volume**: number of patients, admissions count, bed occupancy
- **Clinical**: specific diagnoses, treatment protocols, medication usage
- **Staffing**: nurse-to-patient ratios, physician counts, staff satisfaction
- **Time series**: trend data (CMS Compare is a snapshot, not longitudinal)
- **Individual patients**: any question about specific patient records
