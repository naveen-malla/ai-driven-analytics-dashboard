from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from backend.config import settings


def load_provenance() -> dict:
    """Read provenance.json and return its contents as a dict.

    Returns an empty dict if the file does not exist yet.
    """
    path = Path(settings.PROVENANCE_PATH)
    if not path.exists():
        return {}
    with path.open() as f:
        return json.load(f)


def save_chart_provenance(
    chart_id: str,
    sql: str,
    data: list[dict],
    chart_spec: dict,
    metric_definition: str,
) -> None:
    """Append or update the provenance record for a chart.

    The provenance.json file lives in data/ (owned by the data layer) but is
    written here so that every chart render — static or AI-generated — is
    fully reproducible from its SQL and data snapshot.

    Args:
        chart_id: Unique chart identifier string.
        sql: The validated SQL that produced this chart's data.
        data: The result rows returned by execute_query.
        chart_spec: Serialisable dict representation of the ChartSpec.
        metric_definition: Human-readable metric definition string.
    """
    provenance = load_provenance()
    provenance[chart_id] = {
        "chart_id": chart_id,
        "sql": sql,
        "data_snapshot": data,
        "chart_spec": chart_spec,
        "metric_definition": metric_definition,
        "recorded_at": datetime.now(tz=timezone.utc).isoformat(),
    }

    path = Path(settings.PROVENANCE_PATH)
    # Ensure the parent directory exists (data/ is created by the data phase).
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(provenance, f, indent=2)
