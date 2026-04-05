"""Tests for backend/static_charts.py — chart definitions, SQL structure, contract compliance."""

import pytest
from backend.static_charts import CHART_DEFINITIONS, CHART_IDS, make_chart_spec


EXPECTED_IDS = [
    "contraceptive_prevalence",
    "maternal_mortality",
    "antenatal_care",
    "skilled_birth",
    "under5_mortality",
    "hiv_prevalence",
]


def test_exactly_six_charts():
    assert len(CHART_IDS) == 6


def test_chart_ids_match_contract():
    assert set(CHART_IDS) == set(EXPECTED_IDS)


@pytest.mark.parametrize("chart_id", EXPECTED_IDS)
def test_each_chart_has_required_fields(chart_id):
    defn = CHART_DEFINITIONS[chart_id]
    required = {"chart_id", "title", "chart_type", "x_key", "y_key",
                "metric_definition", "x_label", "y_label", "sql"}
    missing = required - defn.keys()
    assert not missing, f"{chart_id} missing: {missing}"


@pytest.mark.parametrize("chart_id", EXPECTED_IDS)
def test_sql_starts_with_select(chart_id):
    sql = CHART_DEFINITIONS[chart_id]["sql"].strip().upper()
    assert sql.startswith("SELECT")


@pytest.mark.parametrize("chart_id", EXPECTED_IDS)
def test_sql_has_limit(chart_id):
    sql = CHART_DEFINITIONS[chart_id]["sql"].upper()
    assert "LIMIT" in sql


@pytest.mark.parametrize("chart_id", EXPECTED_IDS)
def test_sql_filters_null_values(chart_id):
    sql = CHART_DEFINITIONS[chart_id]["sql"].upper()
    assert "VALUE IS NOT NULL" in sql


@pytest.mark.parametrize("chart_id", EXPECTED_IDS)
def test_sql_filters_btsx(chart_id):
    sql = CHART_DEFINITIONS[chart_id]["sql"]
    assert "BTSX" in sql


@pytest.mark.parametrize("chart_id", EXPECTED_IDS)
def test_x_key_is_country_name(chart_id):
    # All static charts group by country — x axis must be country_name
    assert CHART_DEFINITIONS[chart_id]["x_key"] == "country_name"


@pytest.mark.parametrize("chart_id", EXPECTED_IDS)
def test_y_key_is_value(chart_id):
    assert CHART_DEFINITIONS[chart_id]["y_key"] == "value"


def test_make_chart_spec_returns_correct_shape():
    fake_data = [{"country_name": "Rwanda", "value": 64.2}]
    spec = make_chart_spec("contraceptive_prevalence", fake_data)
    assert spec.chart_id == "contraceptive_prevalence"
    assert spec.data == fake_data
    assert spec.x_key == "country_name"
    assert spec.y_key == "value"


def test_make_chart_spec_accepts_empty_data():
    spec = make_chart_spec("maternal_mortality", [])
    assert spec.data == []
