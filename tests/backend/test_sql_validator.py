"""Tests for backend/sql_validator.py — all 5 checks."""

import pytest
from backend.sql_validator import validate_sql


# ── Check 1: SELECT only ───────────────────────────────────────────────────────

def test_valid_select_passes():
    sql = "SELECT country_name, value FROM country_data LIMIT 10"
    result = validate_sql(sql)
    assert result["valid"] is True


@pytest.mark.parametrize("bad_keyword", [
    "INSERT INTO country_data VALUES (1)",
    "UPDATE country_data SET value = 0",
    "DELETE FROM country_data",
    "DROP TABLE country_data",
    "CREATE TABLE foo (id INT)",
    "TRUNCATE country_data",
])
def test_non_select_rejected(bad_keyword):
    result = validate_sql(bad_keyword)
    assert result["valid"] is False
    assert result["fixed_sql"] is None


# ── Check 2: No semicolons ─────────────────────────────────────────────────────

def test_semicolon_rejected():
    sql = "SELECT * FROM country_data LIMIT 10; DROP TABLE country_data"
    result = validate_sql(sql)
    assert result["valid"] is False
    assert result["fixed_sql"] is None


# ── Check 3: Known tables only ─────────────────────────────────────────────────

def test_known_tables_pass():
    sql = "SELECT cd.value FROM country_data cd JOIN countries c ON cd.country_code = c.country_code LIMIT 5"
    result = validate_sql(sql)
    assert result["valid"] is True


def test_unknown_table_rejected():
    sql = "SELECT * FROM secret_table LIMIT 10"
    result = validate_sql(sql)
    assert result["valid"] is False


def test_all_three_known_tables():
    sql = (
        "SELECT cd.value, c.country_name, i.indicator_name "
        "FROM country_data cd "
        "JOIN countries c ON cd.country_code = c.country_code "
        "JOIN indicators i ON cd.indicator_code = i.indicator_code "
        "LIMIT 10"
    )
    result = validate_sql(sql)
    assert result["valid"] is True


# ── Check 4: LIMIT required ────────────────────────────────────────────────────

def test_missing_limit_gets_fixed():
    sql = "SELECT country_name FROM countries"
    result = validate_sql(sql)
    assert result["valid"] is False
    assert result["fixed_sql"] is not None
    assert "LIMIT" in result["fixed_sql"].upper()


def test_limit_over_500_gets_reduced():
    sql = "SELECT country_name FROM countries LIMIT 1000"
    result = validate_sql(sql)
    assert result["valid"] is False
    assert result["fixed_sql"] is not None
    assert "LIMIT 500" in result["fixed_sql"].upper() or "limit 500" in result["fixed_sql"].lower()


def test_valid_limit_passes():
    sql = "SELECT country_name FROM countries LIMIT 50"
    result = validate_sql(sql)
    assert result["valid"] is True


# ── Check 5: No injection patterns ────────────────────────────────────────────

@pytest.mark.parametrize("injection", [
    "SELECT * FROM countries LIMIT 10 -- drop everything",
    "SELECT * FROM countries /* comment */ LIMIT 10",
    "SELECT * FROM countries LIMIT 10 UNION ALL SELECT * FROM countries",
])
def test_injection_patterns_rejected(injection):
    result = validate_sql(injection)
    assert result["valid"] is False
    assert result["fixed_sql"] is None


# ── Return shape ───────────────────────────────────────────────────────────────

def test_result_always_has_three_keys():
    result = validate_sql("SELECT * FROM countries LIMIT 5")
    assert "valid" in result
    assert "fixed_sql" in result
    assert "reason" in result


def test_valid_result_has_null_fixed_sql_and_reason():
    result = validate_sql("SELECT country_name FROM countries LIMIT 5")
    assert result["valid"] is True
    assert result["fixed_sql"] is None
    assert result["reason"] is None
