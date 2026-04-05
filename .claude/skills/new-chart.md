---
name: new-chart
description: Generate a new analytics chart from a natural language question about hospital quality data. Validates answerability, plans the query, validates SQL, executes it, and returns a Plotly-compatible chart spec.
---

Follow this process **in order** for every new chart request. Do not skip steps.

## Step 1 — Check answerability

Use the `data-analyst` subagent to check if the question can be answered from the WHO GHO schema.

If the analyst returns `answerable: false`, stop here and explain what data would be needed and why it's not available.

## Step 2 — Get query plan

The `data-analyst` subagent returns a structured query plan with tables, columns, joins, filters, aggregation, chart type, and title.

Review the plan:
- Does it make business sense for a CXO?
- Are the filters handling NULL values correctly (`WHERE value IS NOT NULL`)?
- Is the chart type appropriate for the data shape?

## Step 3 — Build and validate SQL

Construct the SQL from the query plan. Then pass it to the `sql-validator` subagent.

If invalid:
- Apply the `fixed_sql` if provided
- Re-validate the fixed version
- If still invalid, explain the issue and stop

## Step 4 — Execute

Use the `execute_sql` tool with the validated SQL. The tool returns rows as a list of dicts.

If execution fails, check:
- Are column names correct (DuckDB normalizes to lowercase with underscores)?
- Is the CAST handling VARCHAR score columns properly?

## Step 5 — Build chart spec

Return a chart spec in this exact format:

```json
{
  "chart_id": "generated_<timestamp>",
  "title": "...",
  "chart_type": "bar | line | scatter | pie | area",
  "sql": "...",
  "x_key": "column_name_for_x_axis",
  "y_key": "column_name_for_y_axis",
  "data": [...],
  "metric_definition": "plain English definition of the metric shown",
  "x_label": "human-readable x axis label",
  "y_label": "human-readable y axis label"
}
```

## Step 6 — Explain the result

After returning the spec, write 2–3 sentences explaining the key insight from the data.

## Rules

- Never return a chart with fewer than 3 data points
- If data is empty after filtering NULL values, explain this clearly rather than returning an empty chart
- Always include the SQL in the spec so the user can verify the result
