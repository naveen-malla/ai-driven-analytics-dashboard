from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.chat_orchestrator import orchestrate
from backend.database import execute_query
from backend.models import ChartsResponse, ChatRequest, ChatResponse, ChartSpec
from backend.provenance import save_chart_provenance
from backend.sql_validator import validate_sql
from backend.static_charts import CHART_DEFINITIONS, CHART_IDS, make_chart_spec

app = FastAPI(
    title="Health Analytics API",
    description="WHO Global Health Observatory analytics dashboard — backend API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _run_chart(chart_id: str) -> ChartSpec:
    """Validate, execute, and persist a single chart's SQL.

    Returns a populated ChartSpec. Raises HTTPException on validation failure
    or database errors.
    """
    defn = CHART_DEFINITIONS[chart_id]
    sql = defn["sql"]

    result = validate_sql(sql)
    if not result["valid"]:
        if result["fixed_sql"]:
            sql = result["fixed_sql"]
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Static chart SQL failed validation: {result['reason']}",
            )

    data = execute_query(sql)
    spec = make_chart_spec(chart_id, data)

    save_chart_provenance(
        chart_id=chart_id,
        sql=sql,
        data=data,
        chart_spec=spec.model_dump(),
        metric_definition=defn["metric_definition"],
    )

    return spec


@app.get("/charts", response_model=ChartsResponse)
def get_charts() -> ChartsResponse:
    """Run all 6 static chart SQLs and return their populated specs."""
    charts: list[ChartSpec] = []
    for chart_id in CHART_IDS:
        charts.append(_run_chart(chart_id))
    return ChartsResponse(charts=charts)


@app.get("/charts/{chart_id}", response_model=ChartSpec)
def get_chart(chart_id: str) -> ChartSpec:
    """Return the populated ChartSpec for a single chart_id.

    Returns 404 if chart_id is not one of the 6 defined charts.
    """
    if chart_id not in CHART_DEFINITIONS:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Chart '{chart_id}' not found. "
                f"Available charts: {', '.join(CHART_IDS)}."
            ),
        )
    return _run_chart(chart_id)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Handle a chat message.

    Stub for Phase 3 — returns a placeholder response while the Claude API
    integration is pending.
    """
    # Phase 3 will route through orchestrate() with real Claude API calls.
    # For now, return a minimal stub so the dashboard can wire up the endpoint.
    return ChatResponse(
        reply="Chat coming in Phase 3",
        chart=None,
        intent="new_analysis",
    )
