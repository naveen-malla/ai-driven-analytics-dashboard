from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ChartSpec(BaseModel):
    chart_id: str
    title: str
    chart_type: str
    x_key: str
    y_key: str
    data: list[dict]
    metric_definition: str
    x_label: str
    y_label: str


class ChartsResponse(BaseModel):
    charts: list[ChartSpec]


class ChatRequest(BaseModel):
    message: str
    chart_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    chart: ChartSpec | None = None
    intent: str


class IntentResult(BaseModel):
    intent: Literal["explain_chart", "new_analysis", "reject"]
    chart_id: str | None
    reasoning: str
