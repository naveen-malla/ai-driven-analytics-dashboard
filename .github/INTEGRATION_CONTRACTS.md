# Integration Contracts v1

Locked 2026-04-05. These are the cross-workstream data shapes. Do not change without updating all affected files.

---

## Contract 1 — GET /charts Response Shape

**Producer**: `backend/main.py`
**Consumer**: `dashboard/api_client.py`

```json
{
  "charts": [
    {
      "chart_id": "contraceptive_prevalence",
      "title": "Contraceptive Prevalence Rate by Country",
      "chart_type": "bar",
      "x_key": "country_name",
      "y_key": "value",
      "data": [
        {"country_name": "Rwanda", "value": 64.2},
        {"country_name": "Kenya", "value": 53.1}
      ],
      "metric_definition": "% of women aged 15–49 using any contraceptive method",
      "x_label": "Country",
      "y_label": "Prevalence (%)"
    }
  ]
}
```

**Rules**:
- `chart_id` is always a `snake_case` string — never an integer
- `data` is always a list of dicts — keys must match `x_key` and `y_key` values
- `data` can be an empty list `[]` if no rows returned — never `null`
- `chart_type` is one of: `bar`, `line`, `scatter`, `area`, `pie`

---

## Contract 2 — The 6 Static Chart IDs

Both `backend/static_charts.py` and `dashboard/components/chart_card.py` must use these exact `chart_id` strings:

| chart_id | Title | WHO Indicator Code | Direction |
|---|---|---|---|
| `contraceptive_prevalence` | Contraceptive Prevalence Rate by Country | FP_CXUS_W_CURR | Higher = better |
| `maternal_mortality` | Maternal Mortality Ratio by Country | MDG_0000000025 | Lower = better |
| `antenatal_care` | Antenatal Care Coverage by Country | MDG_0000000031 | Higher = better |
| `skilled_birth` | Skilled Birth Attendance by Country | MDG_0000000032 | Higher = better |
| `under5_mortality` | Under-5 Mortality Rate by Country | MDG_0000000001 | Lower = better |
| `hiv_prevalence` | HIV Prevalence by Country | HIV_0000000026 | Lower = better |

---

## Contract 3 — schema_registry.json Format

**Producer**: `data/load_who.py` (Pathey writes this)
**Consumer**: `backend/schema_loader.py` (Naveen reads this)

```json
{
  "tables": {
    "country_data": {
      "description": "WHO GHO health indicator values by country and year",
      "columns": {
        "country_code": {
          "type": "VARCHAR",
          "description": "ISO 3-letter country code (RWA, KEN, UGA, ETH, TZA)",
          "example_values": ["RWA", "KEN", "ETH"]
        },
        "indicator_code": {
          "type": "VARCHAR",
          "description": "WHO GHO indicator code",
          "example_values": ["FP_CXUS_W_CURR", "MDG_0000000025"]
        },
        "year": {
          "type": "INTEGER",
          "description": "Year of measurement",
          "example_values": ["2020", "2019"]
        },
        "value": {
          "type": "FLOAT",
          "description": "Indicator value — may be NULL for some country/year combinations",
          "example_values": ["64.2", "41.0"]
        },
        "sex": {
          "type": "VARCHAR",
          "description": "Sex disaggregation: BTSX (both sexes), MLE (male), FMLE (female). Use BTSX for summary charts.",
          "example_values": ["BTSX", "MLE", "FMLE"]
        }
      }
    },
    "countries": {
      "description": "Country reference table",
      "columns": {
        "country_code": {
          "type": "VARCHAR",
          "description": "ISO 3-letter country code — primary key",
          "example_values": ["RWA", "KEN"]
        },
        "country_name": {
          "type": "VARCHAR",
          "description": "Full country name",
          "example_values": ["Rwanda", "Kenya"]
        }
      }
    },
    "indicators": {
      "description": "Indicator reference table",
      "columns": {
        "indicator_code": {
          "type": "VARCHAR",
          "description": "WHO GHO indicator code — primary key",
          "example_values": ["FP_CXUS_W_CURR"]
        },
        "indicator_name": {
          "type": "VARCHAR",
          "description": "Human-readable indicator name",
          "example_values": ["Contraceptive prevalence, any method (%)"]
        },
        "unit": {
          "type": "VARCHAR",
          "description": "Unit of measurement",
          "example_values": ["%", "per 100 000 live births"]
        }
      }
    }
  },
  "allowed_joins": [
    {
      "from_table": "country_data",
      "to_table": "countries",
      "on": "country_data.country_code = countries.country_code",
      "description": "Join health indicator values to country names"
    },
    {
      "from_table": "country_data",
      "to_table": "indicators",
      "on": "country_data.indicator_code = indicators.indicator_code",
      "description": "Join health indicator values to indicator metadata"
    }
  ],
  "business_context": "WHO Global Health Observatory data for Kasha's 5 core markets in East Africa. Covers reproductive health, maternal health, and child health indicators. Data is cross-sectional by year — not all indicators have data for every country/year.",
  "not_answerable": [
    "Individual patient or person records",
    "Drug pricing, procurement costs, or supply chain data",
    "Country-specific clinical protocols or treatment guidelines",
    "Forecasts or projections beyond available data years",
    "Questions requiring data from countries outside RWA, KEN, UGA, ETH, TZA"
  ]
}
```

---

## Contract 4 — POST /chat Request/Response (Phase 3)

**Producer**: `backend/main.py`
**Consumer**: `dashboard/api_client.py`

Request:
```json
{
  "message": "What is the contraceptive prevalence in Rwanda?",
  "chart_id": "contraceptive_prevalence"
}
```

`chart_id` is `null` for new questions not tied to an existing chart.

Response:
```json
{
  "reply": "Plain English explanation or analysis result",
  "chart": null,
  "intent": "explain_chart | new_analysis | reject"
}
```

When `intent = "new_analysis"`, `chart` is a full chart object with the same shape as Contract 1.

---

## Contract 5 — Backend URL

- Development: `http://localhost:8000`
- Only `dashboard/api_client.py` holds this URL — nowhere else in dashboard/ code
