"""
Shared test fixtures for the health analytics dashboard test suite.

Usage:
    These fixtures are automatically available in all test files.
    No imports needed — pytest discovers conftest.py automatically.
"""

import json
import pytest
import duckdb
from fastapi.testclient import TestClient


# ── In-memory DuckDB with fixture data ────────────────────────────────────────

@pytest.fixture
def test_db():
    """
    Create a temporary in-memory DuckDB with the full schema and a small
    set of realistic fixture rows. Yields the connection; closes after test.

    Tests that call execute_query() should patch backend.database._connection
    with this fixture using monkeypatch.
    """
    conn = duckdb.connect(":memory:")

    conn.execute("""
        CREATE TABLE countries (
            country_code VARCHAR PRIMARY KEY,
            country_name VARCHAR NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE indicators (
            indicator_code VARCHAR PRIMARY KEY,
            indicator_name VARCHAR NOT NULL,
            unit VARCHAR
        )
    """)
    conn.execute("""
        CREATE TABLE country_data (
            country_code VARCHAR NOT NULL,
            indicator_code VARCHAR NOT NULL,
            year INTEGER NOT NULL,
            value FLOAT,
            sex VARCHAR,
            low_estimate FLOAT,
            high_estimate FLOAT
        )
    """)

    # Seed countries
    conn.executemany(
        "INSERT INTO countries VALUES (?, ?)",
        [
            ("RWA", "Rwanda"),
            ("KEN", "Kenya"),
            ("UGA", "Uganda"),
            ("ETH", "Ethiopia"),
            ("TZA", "Tanzania"),
        ],
    )

    # Seed indicators
    conn.executemany(
        "INSERT INTO indicators VALUES (?, ?, ?)",
        [
            ("FP_CXUS_W_CURR", "Contraceptive prevalence, any method (%)", "%"),
            ("MDG_0000000025", "Maternal mortality ratio", "per 100 000 live births"),
            ("MDG_0000000031", "Antenatal care coverage - at least four visits (%)", "%"),
            ("MDG_0000000032", "Births attended by skilled health personnel (%)", "%"),
            ("MDG_0000000001", "Under-five mortality rate (per 1000 live births)", "per 1000"),
            ("HIV_0000000026", "Prevalence of HIV among adults aged 15 to 49 (%)", "%"),
        ],
    )

    # Seed country_data — one row per country per indicator, all BTSX, year 2020
    rows = [
        # contraceptive prevalence
        ("RWA", "FP_CXUS_W_CURR", 2020, 64.2, "BTSX", None, None),
        ("KEN", "FP_CXUS_W_CURR", 2020, 53.1, "BTSX", None, None),
        ("UGA", "FP_CXUS_W_CURR", 2020, 47.8, "BTSX", None, None),
        ("ETH", "FP_CXUS_W_CURR", 2020, 41.0, "BTSX", None, None),
        ("TZA", "FP_CXUS_W_CURR", 2020, 38.4, "BTSX", None, None),
        # maternal mortality
        ("RWA", "MDG_0000000025", 2020, 203.0, "BTSX", None, None),
        ("KEN", "MDG_0000000025", 2020, 342.0, "BTSX", None, None),
        ("UGA", "MDG_0000000025", 2020, 287.0, "BTSX", None, None),
        ("ETH", "MDG_0000000025", 2020, 401.0, "BTSX", None, None),
        ("TZA", "MDG_0000000025", 2020, 524.0, "BTSX", None, None),
        # antenatal care
        ("RWA", "MDG_0000000031", 2020, 44.7, "BTSX", None, None),
        ("KEN", "MDG_0000000031", 2020, 56.0, "BTSX", None, None),
        ("UGA", "MDG_0000000031", 2020, 60.1, "BTSX", None, None),
        ("ETH", "MDG_0000000031", 2020, 43.3, "BTSX", None, None),
        ("TZA", "MDG_0000000031", 2020, 51.8, "BTSX", None, None),
        # skilled birth
        ("RWA", "MDG_0000000032", 2020, 91.0, "BTSX", None, None),
        ("KEN", "MDG_0000000032", 2020, 62.0, "BTSX", None, None),
        ("UGA", "MDG_0000000032", 2020, 74.0, "BTSX", None, None),
        ("ETH", "MDG_0000000032", 2020, 28.0, "BTSX", None, None),
        ("TZA", "MDG_0000000032", 2020, 64.0, "BTSX", None, None),
        # under5 mortality
        ("RWA", "MDG_0000000001", 2020, 36.0, "BTSX", None, None),
        ("KEN", "MDG_0000000001", 2020, 43.0, "BTSX", None, None),
        ("UGA", "MDG_0000000001", 2020, 57.0, "BTSX", None, None),
        ("ETH", "MDG_0000000001", 2020, 51.0, "BTSX", None, None),
        ("TZA", "MDG_0000000001", 2020, 52.0, "BTSX", None, None),
        # hiv prevalence
        ("RWA", "HIV_0000000026", 2020, 2.5, "BTSX", None, None),
        ("KEN", "HIV_0000000026", 2020, 4.3, "BTSX", None, None),
        ("UGA", "HIV_0000000026", 2020, 5.4, "BTSX", None, None),
        ("ETH", "HIV_0000000026", 2020, 0.9, "BTSX", None, None),
        ("TZA", "HIV_0000000026", 2020, 4.7, "BTSX", None, None),
    ]
    conn.executemany(
        "INSERT INTO country_data VALUES (?, ?, ?, ?, ?, ?, ?)", rows
    )

    yield conn
    conn.close()


@pytest.fixture
def patched_db(test_db, monkeypatch):
    """
    Patches backend.database._connection with the in-memory test DB.
    Use this in any test that exercises code calling execute_query().
    """
    import backend.database as db_module
    monkeypatch.setattr(db_module, "_connection", test_db)
    return test_db


@pytest.fixture
def api_client(patched_db):
    """
    FastAPI TestClient with the in-memory DB already wired in.
    Use for testing HTTP routes without a real database or server.
    """
    from backend.main import app
    return TestClient(app)
