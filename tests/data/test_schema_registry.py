"""Tests for data/schema_registry.json — validates structure matches integration contracts."""

import json
from pathlib import Path

import pytest

REGISTRY_PATH = Path("data/schema_registry.json")
EXPECTED_TABLES = {"country_data", "countries", "indicators"}
EXPECTED_COUNTRY_DATA_COLUMNS = {"country_code", "indicator_code", "year", "value", "sex"}


@pytest.fixture
def registry():
    assert REGISTRY_PATH.exists(), f"schema_registry.json not found at {REGISTRY_PATH.resolve()}"
    with REGISTRY_PATH.open() as f:
        return json.load(f)


def test_registry_has_tables_key(registry):
    assert "tables" in registry, "schema_registry.json must have a 'tables' key"


def test_registry_has_allowed_joins_key(registry):
    assert "allowed_joins" in registry, "schema_registry.json must have 'allowed_joins' (not 'joins')"


def test_registry_has_all_three_tables(registry):
    tables = set(registry["tables"].keys())
    missing = EXPECTED_TABLES - tables
    assert not missing, f"Missing tables: {missing}"


def test_country_data_has_required_columns(registry):
    columns = set(registry["tables"]["country_data"]["columns"].keys())
    missing = EXPECTED_COUNTRY_DATA_COLUMNS - columns
    assert not missing, f"country_data missing columns: {missing}"


def test_countries_has_country_code_and_name(registry):
    columns = set(registry["tables"]["countries"]["columns"].keys())
    assert "country_code" in columns
    assert "country_name" in columns


def test_indicators_has_indicator_code(registry):
    columns = set(registry["tables"]["indicators"]["columns"].keys())
    assert "indicator_code" in columns


def test_allowed_joins_is_list(registry):
    assert isinstance(registry["allowed_joins"], list)


def test_allowed_joins_not_empty(registry):
    assert len(registry["allowed_joins"]) >= 2, "Must have at least 2 joins documented"


def test_each_join_has_required_keys(registry):
    for join in registry["allowed_joins"]:
        assert "from_table" in join, f"Join missing 'from_table': {join}"
        assert "to_table" in join, f"Join missing 'to_table': {join}"
        assert "on" in join, f"Join missing 'on': {join}"


def test_country_data_to_countries_join_exists(registry):
    joins = registry["allowed_joins"]
    has_join = any(
        j.get("from_table") == "country_data" and j.get("to_table") == "countries"
        for j in joins
    )
    assert has_join, "Must have country_data → countries join"


def test_country_data_to_indicators_join_exists(registry):
    joins = registry["allowed_joins"]
    has_join = any(
        j.get("from_table") == "country_data" and j.get("to_table") == "indicators"
        for j in joins
    )
    assert has_join, "Must have country_data → indicators join"


def test_each_table_has_description(registry):
    for table_name, table_info in registry["tables"].items():
        assert "description" in table_info, f"Table '{table_name}' missing 'description'"
        assert len(table_info["description"]) > 10


def test_each_column_has_type_and_description(registry):
    for table_name, table_info in registry["tables"].items():
        for col_name, col_info in table_info.get("columns", {}).items():
            assert "type" in col_info, f"{table_name}.{col_name} missing 'type'"
            assert "description" in col_info, f"{table_name}.{col_name} missing 'description'"
