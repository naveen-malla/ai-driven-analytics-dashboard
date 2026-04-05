"""
WHO Global Health Observatory ingestion script.

Usage:
    python data/load_who.py

Run from the repo root. Creates (or recreates) data/who_health.duckdb with
three tables: countries, indicators, country_data.

The script is idempotent — it drops and recreates all tables on each run.
No external dependencies beyond what's in requirements.txt (requests, duckdb).
"""

import requests
import duckdb
import os
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DB_PATH = os.path.join(os.path.dirname(__file__), "who_health.duckdb")

BASE_URL = "https://ghoapi.azureedge.net/api"

TARGET_COUNTRIES = {"RWA", "KEN", "UGA", "ETH", "TZA"}

COUNTRY_NAMES = {
    "RWA": "Rwanda",
    "KEN": "Kenya",
    "UGA": "Uganda",
    "ETH": "Ethiopia",
    "TZA": "Tanzania",
}

# (indicator_code, indicator_name, unit)
INDICATORS = [
    ("FP_CXUS_W_CURR",   "Contraceptive prevalence, any method",                        "%"),
    ("MDG_0000000025",    "Maternal mortality ratio",                                    "per 100 000 live births"),
    ("MDG_0000000031",    "Antenatal care coverage (4+ visits)",                         "%"),
    ("MDG_0000000032",    "Births attended by skilled health personnel",                 "%"),
    ("MDG_0000000001",    "Under-5 mortality rate",                                      "per 1000 live births"),
    ("HIV_0000000026",    "HIV prevalence among adults aged 15-49 years (%)",            "%"),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_indicator(indicator_code: str) -> list[dict]:
    """Fetch all country-level rows for one WHO GHO indicator.

    Returns the raw list of value dicts from the API response.
    Returns [] on HTTP error so the caller can continue with other indicators.

    Data quality notes:
    - NumericValue may be None for some country/year combinations.
    - Low/High confidence intervals are often None even when NumericValue is present.
    - Dim1 encodes sex disaggregation: BTSX = both sexes, MLE = male, FMLE = female.
      Use BTSX rows for summary charts.
    """
    url = f"{BASE_URL}/{indicator_code}?$filter=SpatialDimType eq 'COUNTRY'"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json().get("value", [])
    except requests.HTTPError as exc:
        print(f"  WARNING: HTTP error for {indicator_code}: {exc}", file=sys.stderr)
        return []
    except requests.RequestException as exc:
        print(f"  WARNING: Request failed for {indicator_code}: {exc}", file=sys.stderr)
        return []


def filter_to_target_countries(rows: list[dict]) -> list[dict]:
    """Keep only rows for the 5 target countries."""
    return [r for r in rows if r.get("SpatialDim") in TARGET_COUNTRIES]


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def create_schema(con: duckdb.DuckDBPyConnection) -> None:
    """Drop and recreate all three tables (idempotent)."""
    con.execute("DROP TABLE IF EXISTS country_data")
    con.execute("DROP TABLE IF EXISTS countries")
    con.execute("DROP TABLE IF EXISTS indicators")

    con.execute("""
        CREATE TABLE countries (
            country_code VARCHAR PRIMARY KEY,
            country_name VARCHAR NOT NULL
        )
    """)

    con.execute("""
        CREATE TABLE indicators (
            indicator_code VARCHAR PRIMARY KEY,
            indicator_name VARCHAR NOT NULL,
            unit           VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE country_data (
            country_code   VARCHAR NOT NULL,
            indicator_code VARCHAR NOT NULL,
            year           INTEGER NOT NULL,
            value          FLOAT,
            sex            VARCHAR,
            low_estimate   FLOAT,
            high_estimate  FLOAT
        )
    """)


def load_reference_tables(con: duckdb.DuckDBPyConnection) -> None:
    """Populate countries and indicators with hardcoded reference data."""
    for code, name in COUNTRY_NAMES.items():
        con.execute(
            "INSERT INTO countries VALUES (?, ?)",
            [code, name],
        )

    for code, name, unit in INDICATORS:
        con.execute(
            "INSERT INTO indicators VALUES (?, ?, ?)",
            [code, name, unit],
        )


# ---------------------------------------------------------------------------
# Main ingestion
# ---------------------------------------------------------------------------

def load_indicator_data(
    con: duckdb.DuckDBPyConnection,
    indicator_code: str,
    indicator_name: str,
) -> int:
    """Fetch one indicator from WHO GHO, filter to target countries, insert rows.

    Returns the number of rows inserted.
    """
    print(f"  Fetching {indicator_code} ({indicator_name}) ...", end=" ", flush=True)
    all_rows = fetch_indicator(indicator_code)
    rows = filter_to_target_countries(all_rows)

    inserted = 0
    for r in rows:
        value = r.get("NumericValue")
        low   = r.get("Low")
        high  = r.get("High")
        sex   = r.get("Dim1")  # BTSX / MLE / FMLE or None
        year  = r.get("TimeDim")
        country_code = r.get("SpatialDim")

        if year is None or country_code is None:
            # Skip malformed rows
            continue

        con.execute(
            """
            INSERT INTO country_data
                (country_code, indicator_code, year, value, sex, low_estimate, high_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [country_code, indicator_code, int(year), value, sex, low, high],
        )
        inserted += 1

    print(f"{inserted} rows loaded.")
    return inserted


def main() -> None:
    print(f"Opening DuckDB at: {DB_PATH}")
    con = duckdb.connect(DB_PATH)

    print("Creating schema (drop + recreate) ...")
    create_schema(con)

    print("Loading reference tables ...")
    load_reference_tables(con)
    print(f"  {len(COUNTRY_NAMES)} countries loaded.")
    print(f"  {len(INDICATORS)} indicators loaded.")

    print("\nIngesting WHO GHO data ...")
    total_rows = 0
    for code, name, _ in INDICATORS:
        total_rows += load_indicator_data(con, code, name)

    print(f"\nDone. Total country_data rows inserted: {total_rows}")

    # Quick sanity check
    row_count = con.execute("SELECT COUNT(*) FROM country_data").fetchone()[0]
    countries_present = con.execute(
        "SELECT COUNT(DISTINCT country_code) FROM country_data"
    ).fetchone()[0]
    indicators_present = con.execute(
        "SELECT COUNT(DISTINCT indicator_code) FROM country_data"
    ).fetchone()[0]

    print(f"\nSanity check:")
    print(f"  country_data rows   : {row_count}")
    print(f"  distinct countries  : {countries_present} (expected 5)")
    print(f"  distinct indicators : {indicators_present} (expected 6)")

    con.close()
    print("\nIngestion complete.")


if __name__ == "__main__":
    main()
