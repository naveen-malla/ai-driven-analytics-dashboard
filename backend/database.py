from __future__ import annotations

import os
from pathlib import Path

import duckdb

from backend.config import settings

_connection: duckdb.DuckDBPyConnection | None = None


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return the shared read-only DuckDB connection, creating it on first call."""
    global _connection
    if _connection is None:
        db_path = Path(settings.DB_PATH)
        if not db_path.exists():
            raise FileNotFoundError(
                f"Database file not found at '{db_path.resolve()}'. "
                "Run the data ingestion script (data/load_who.py) first to create it."
            )
        _connection = duckdb.connect(str(db_path), read_only=True)
    return _connection


def execute_query(sql: str, params: list | None = None) -> list[dict]:
    """Execute a SQL query and return results as a list of row dicts.

    Args:
        sql: A validated SELECT query.
        params: Optional positional parameters for parameterised queries.

    Returns:
        A list of dicts, one per row, with column names as keys.
    """
    conn = get_connection()
    if params:
        result = conn.execute(sql, params)
    else:
        result = conn.execute(sql)
    columns = [desc[0] for desc in result.description]
    rows = result.fetchall()
    return [dict(zip(columns, row)) for row in rows]
