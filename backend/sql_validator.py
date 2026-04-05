from __future__ import annotations

import re

# Tables permitted by the schema registry.
_ALLOWED_TABLES = {"countries", "indicators", "country_data"}

# Patterns that indicate injection attempts (case-insensitive where noted).
_INJECTION_PATTERNS = [
    "--",
    "/*",
    "*/",
    "xp_",
    "exec(",
    "union all select",  # checked case-insensitively
    "drop table",        # checked case-insensitively
    "'; --",
]

# DML/DDL keywords that must never appear as the leading operation.
_DISALLOWED_STARTS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "CREATE",
    "DROP",
    "TRUNCATE",
    "COPY",
    "ALTER",
    "GRANT",
    "REVOKE",
    "EXECUTE",
    "CALL",
]

_LIMIT_RE = re.compile(r"\bLIMIT\s+(\d+)\b", re.IGNORECASE)
_TABLE_REF_RE = re.compile(r"\b(?:FROM|JOIN)\s+(\w+)", re.IGNORECASE)


def validate_sql(sql: str) -> dict:
    """Validate a SQL query against all 5 safety checks.

    Returns a dict with keys:
        valid (bool): True only when the query is safe to execute as-is.
        fixed_sql (str | None): A corrected query when the only issue was
            a missing or oversized LIMIT clause; None otherwise.
        reason (str | None): Human-readable explanation for any failure.
    """
    stripped = sql.strip()

    # ------------------------------------------------------------------ #
    # Check 1 — Must start with SELECT                                     #
    # ------------------------------------------------------------------ #
    first_word = stripped.split()[0].upper() if stripped.split() else ""
    if first_word != "SELECT":
        return {
            "valid": False,
            "fixed_sql": None,
            "reason": (
                f"Query must start with SELECT. "
                f"Found '{first_word}' — only read-only queries are allowed."
            ),
        }

    # Also reject if any disallowed keyword appears at word boundaries
    # (catches e.g. `SELECT 1; DROP TABLE foo`).
    upper_sql = stripped.upper()
    for kw in _DISALLOWED_STARTS:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, upper_sql):
            return {
                "valid": False,
                "fixed_sql": None,
                "reason": (
                    f"Query contains disallowed keyword '{kw}' — "
                    "only SELECT statements are permitted."
                ),
            }

    # ------------------------------------------------------------------ #
    # Check 2 — No semicolons                                              #
    # ------------------------------------------------------------------ #
    if ";" in stripped:
        return {
            "valid": False,
            "fixed_sql": None,
            "reason": "Semicolons are not allowed — multi-statement queries are blocked.",
        }

    # ------------------------------------------------------------------ #
    # Check 3 — Known tables only                                          #
    # ------------------------------------------------------------------ #
    referenced_tables = {m.lower() for m in _TABLE_REF_RE.findall(stripped)}
    unknown_tables = referenced_tables - _ALLOWED_TABLES
    if unknown_tables:
        return {
            "valid": False,
            "fixed_sql": None,
            "reason": (
                f"Unknown table(s) referenced: {', '.join(sorted(unknown_tables))}. "
                f"Allowed tables are: {', '.join(sorted(_ALLOWED_TABLES))}."
            ),
        }

    # ------------------------------------------------------------------ #
    # Check 4 — LIMIT clause present and within bounds                    #
    # ------------------------------------------------------------------ #
    limit_matches = _LIMIT_RE.findall(stripped)
    if not limit_matches:
        # Fixable: add LIMIT 100
        fixed = stripped + " LIMIT 100"
        return {
            "valid": False,
            "fixed_sql": fixed,
            "reason": "Missing LIMIT clause — added LIMIT 100.",
        }

    limit_value = int(limit_matches[-1])
    if limit_value > 500:
        fixed = _LIMIT_RE.sub("LIMIT 500", stripped)
        return {
            "valid": False,
            "fixed_sql": fixed,
            "reason": f"LIMIT {limit_value} exceeds maximum of 500 — reduced to 500.",
        }

    # ------------------------------------------------------------------ #
    # Check 5 — No injection patterns                                      #
    # ------------------------------------------------------------------ #
    lower_sql = stripped.lower()
    for pattern in _INJECTION_PATTERNS:
        if pattern in lower_sql:
            return {
                "valid": False,
                "fixed_sql": None,
                "reason": (
                    f"Injection pattern detected: '{pattern}'. Query rejected."
                ),
            }

    return {"valid": True, "fixed_sql": None, "reason": None}
