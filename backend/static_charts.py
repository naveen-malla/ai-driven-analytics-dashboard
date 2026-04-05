from __future__ import annotations

from backend.models import ChartSpec

# Chart IDs are the integration contract with dashboard/components/chart_card.py.
# Do NOT rename these strings without updating the dashboard contract.

_CHARTS: list[dict] = [
    {
        "chart_id": "contraceptive_prevalence",
        "title": "Contraceptive Prevalence",
        "chart_type": "bar",
        "x_key": "country_name",
        "y_key": "value",
        "metric_definition": (
            "Percentage of women aged 15–49 who are using (or whose partner is using) "
            "a contraceptive method. WHO indicator: FP_CXUS_W_CURR. Higher is better."
        ),
        "x_label": "Country",
        "y_label": "Prevalence (%)",
        "sql": """
SELECT c.country_name, cd.value
FROM country_data cd
JOIN countries c ON cd.country_code = c.country_code
WHERE cd.indicator_code = 'FP_CXUS_W_CURR'
  AND cd.sex = 'BTSX'
  AND cd.value IS NOT NULL
  AND cd.year = (
    SELECT MAX(year) FROM country_data
    WHERE indicator_code = 'FP_CXUS_W_CURR'
      AND value IS NOT NULL AND sex = 'BTSX'
  )
ORDER BY cd.value DESC
LIMIT 10
""".strip(),
    },
    {
        "chart_id": "maternal_mortality",
        "title": "Maternal Mortality Ratio",
        "chart_type": "bar",
        "x_key": "country_name",
        "y_key": "value",
        "metric_definition": (
            "Maternal deaths per 100,000 live births. "
            "WHO indicator: MDG_0000000025. Lower is better."
        ),
        "x_label": "Country",
        "y_label": "Deaths per 100,000 live births",
        "sql": """
SELECT c.country_name, cd.value
FROM country_data cd
JOIN countries c ON cd.country_code = c.country_code
WHERE cd.indicator_code = 'MDG_0000000025'
  AND cd.sex = 'BTSX'
  AND cd.value IS NOT NULL
  AND cd.year = (
    SELECT MAX(year) FROM country_data
    WHERE indicator_code = 'MDG_0000000025'
      AND value IS NOT NULL AND sex = 'BTSX'
  )
ORDER BY cd.value ASC
LIMIT 10
""".strip(),
    },
    {
        "chart_id": "antenatal_care",
        "title": "Antenatal Care Coverage",
        "chart_type": "bar",
        "x_key": "country_name",
        "y_key": "value",
        "metric_definition": (
            "Percentage of pregnant women who received four or more antenatal care visits. "
            "WHO indicator: MDG_0000000031. Higher is better."
        ),
        "x_label": "Country",
        "y_label": "Coverage (%)",
        "sql": """
SELECT c.country_name, cd.value
FROM country_data cd
JOIN countries c ON cd.country_code = c.country_code
WHERE cd.indicator_code = 'MDG_0000000031'
  AND cd.sex = 'BTSX'
  AND cd.value IS NOT NULL
  AND cd.year = (
    SELECT MAX(year) FROM country_data
    WHERE indicator_code = 'MDG_0000000031'
      AND value IS NOT NULL AND sex = 'BTSX'
  )
ORDER BY cd.value DESC
LIMIT 10
""".strip(),
    },
    {
        "chart_id": "skilled_birth",
        "title": "Skilled Birth Attendance",
        "chart_type": "bar",
        "x_key": "country_name",
        "y_key": "value",
        "metric_definition": (
            "Percentage of births attended by skilled health personnel "
            "(doctors, nurses, midwives). "
            "WHO indicator: MDG_0000000032. Higher is better."
        ),
        "x_label": "Country",
        "y_label": "Attendance (%)",
        "sql": """
SELECT c.country_name, cd.value
FROM country_data cd
JOIN countries c ON cd.country_code = c.country_code
WHERE cd.indicator_code = 'MDG_0000000032'
  AND cd.sex = 'BTSX'
  AND cd.value IS NOT NULL
  AND cd.year = (
    SELECT MAX(year) FROM country_data
    WHERE indicator_code = 'MDG_0000000032'
      AND value IS NOT NULL AND sex = 'BTSX'
  )
ORDER BY cd.value DESC
LIMIT 10
""".strip(),
    },
    {
        "chart_id": "under5_mortality",
        "title": "Under-5 Mortality Rate",
        "chart_type": "bar",
        "x_key": "country_name",
        "y_key": "value",
        "metric_definition": (
            "Deaths per 1,000 live births for children under five years of age. "
            "WHO indicator: MDG_0000000001. Lower is better."
        ),
        "x_label": "Country",
        "y_label": "Deaths per 1,000 live births",
        "sql": """
SELECT c.country_name, cd.value
FROM country_data cd
JOIN countries c ON cd.country_code = c.country_code
WHERE cd.indicator_code = 'MDG_0000000001'
  AND cd.sex = 'BTSX'
  AND cd.value IS NOT NULL
  AND cd.year = (
    SELECT MAX(year) FROM country_data
    WHERE indicator_code = 'MDG_0000000001'
      AND value IS NOT NULL AND sex = 'BTSX'
  )
ORDER BY cd.value ASC
LIMIT 10
""".strip(),
    },
    {
        "chart_id": "hiv_prevalence",
        "title": "HIV Prevalence",
        "chart_type": "bar",
        "x_key": "country_name",
        "y_key": "value",
        "metric_definition": (
            "Percentage of adults aged 15–49 living with HIV. "
            "WHO indicator: HIV_0000000026. Lower is better."
        ),
        "x_label": "Country",
        "y_label": "Prevalence (%)",
        "sql": """
SELECT c.country_name, cd.value
FROM country_data cd
JOIN countries c ON cd.country_code = c.country_code
WHERE cd.indicator_code = 'HIV_0000000026'
  AND cd.sex = 'BTSX'
  AND cd.value IS NOT NULL
  AND cd.year = (
    SELECT MAX(year) FROM country_data
    WHERE indicator_code = 'HIV_0000000026'
      AND value IS NOT NULL AND sex = 'BTSX'
  )
ORDER BY cd.value ASC
LIMIT 10
""".strip(),
    },
]

# Index by chart_id for O(1) lookup.
CHART_DEFINITIONS: dict[str, dict] = {c["chart_id"]: c for c in _CHARTS}
CHART_IDS: list[str] = [c["chart_id"] for c in _CHARTS]


def get_chart_sql(chart_id: str) -> str:
    """Return the SQL for a given chart_id.

    Raises KeyError if chart_id is not one of the 6 defined charts.
    """
    return CHART_DEFINITIONS[chart_id]["sql"]


def make_chart_spec(chart_id: str, data: list[dict]) -> ChartSpec:
    """Build a ChartSpec for the given chart_id with the provided data rows."""
    defn = CHART_DEFINITIONS[chart_id]
    return ChartSpec(
        chart_id=defn["chart_id"],
        title=defn["title"],
        chart_type=defn["chart_type"],
        x_key=defn["x_key"],
        y_key=defn["y_key"],
        data=data,
        metric_definition=defn["metric_definition"],
        x_label=defn["x_label"],
        y_label=defn["y_label"],
    )
