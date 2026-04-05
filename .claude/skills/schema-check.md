---
name: schema-check
description: Check if a natural language question can be answered from the available WHO GHO health indicators schema. Returns answerable/not-answerable/partial with exact table and column names, and explains what is missing if not answerable.
---

Read `data/schema_registry.json` first. Then, given a natural language question:

## Step 1 — Identify required data dimensions

What dimensions does this question need?
- A metric (what to measure)
- A grouping dimension (by country, by indicator, by sex, by year, etc.)
- A time dimension (latest year, specific year, or year-over-year comparison)
- A filter (specific indicator code, country code, sex, etc.)

## Step 2 — Map to available schema

For each required dimension, find the exact table and column name in the schema.

## Step 3 — Classify and respond

**Answerable** — all required dimensions exist:
```
ANSWERABLE
Tables: countries, country_data
Key columns: countries.country_name, country_data.value, country_data.indicator_code, country_data.year
Notes: always filter WHERE value IS NOT NULL; use sex = 'BTSX' for both-sexes aggregations
```

**Not answerable** — required data is missing:
```
NOT ANSWERABLE
Missing: [describe what data would be needed]
Reason: WHO GHO data does not include [individual patient records / drug pricing / supply chain / country-specific clinical protocols / etc.]
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

- **Financial**: drug pricing, cost per treatment, revenue, reimbursement rates
- **Individual records**: any question about specific patient or person records
- **Clinical protocols**: country-specific treatment guidelines, medication dosage data
- **Supply chain / logistics**: stock levels, distribution routes, procurement data
- **Outside tracked countries**: questions requiring data from countries other than RWA, KEN, UGA, ETH, TZA
- **Forecasting**: predictions or projections not derivable from the available indicator values
- **Time series**: trend data only available if multiple years exist for the indicator in `country_data`
