from __future__ import annotations

import json
from pathlib import Path

from backend.config import settings

_schema_registry: dict | None = None
_schema_digest: str | None = None


def load_schema_registry() -> dict:
    """Read and return the parsed schema_registry.json.

    Raises FileNotFoundError if the file has not been created yet
    (Pathey creates it during the data phase).
    """
    global _schema_registry
    if _schema_registry is None:
        registry_path = Path(settings.SCHEMA_REGISTRY_PATH)
        if not registry_path.exists():
            raise FileNotFoundError(
                f"Schema registry not found at '{registry_path.resolve()}'. "
                "Run the data ingestion script (data/load_who.py) first."
            )
        with registry_path.open() as f:
            _schema_registry = json.load(f)
    return _schema_registry


def build_schema_digest() -> str:
    """Format the schema registry into a human-readable string for LLM system prompts.

    The result is cached after the first call (compute once per process startup).

    Returns:
        A multiline string listing each table, its description, and its columns
        with types and descriptions — suitable for placement in a system prompt
        with prompt caching.
    """
    global _schema_digest
    if _schema_digest is not None:
        return _schema_digest

    registry = load_schema_registry()
    lines: list[str] = ["## Database Schema\n"]

    tables = registry.get("tables", {})
    for table_name, table_info in tables.items():
        description = table_info.get("description", "No description provided.")
        lines.append(f"### Table: {table_name}")
        lines.append(f"{description}\n")
        lines.append("Columns:")
        columns = table_info.get("columns", {})
        for col_name, col_info in columns.items():
            col_type = col_info.get("type", "unknown")
            col_desc = col_info.get("description", "")
            lines.append(f"  - {col_name} ({col_type}): {col_desc}")
        lines.append("")

    joins = registry.get("joins", [])
    if joins:
        lines.append("## Allowed Joins")
        for join in joins:
            lines.append(f"  - {join}")
        lines.append("")

    _schema_digest = "\n".join(lines)
    return _schema_digest
