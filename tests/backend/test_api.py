"""Tests for FastAPI routes — GET /charts, GET /charts/{id}, POST /chat."""

import pytest
from backend.static_charts import CHART_IDS


# ── GET /charts ────────────────────────────────────────────────────────────────

def test_get_charts_returns_200(api_client):
    response = api_client.get("/charts")
    assert response.status_code == 200


def test_get_charts_returns_charts_key(api_client):
    data = api_client.get("/charts").json()
    assert "charts" in data


def test_get_charts_returns_all_six(api_client):
    data = api_client.get("/charts").json()
    assert len(data["charts"]) == 6


def test_get_charts_all_ids_present(api_client):
    data = api_client.get("/charts").json()
    returned_ids = {c["chart_id"] for c in data["charts"]}
    assert returned_ids == set(CHART_IDS)


def test_get_charts_each_has_required_fields(api_client):
    required = {"chart_id", "title", "chart_type", "x_key", "y_key",
                "data", "metric_definition", "x_label", "y_label"}
    data = api_client.get("/charts").json()
    for chart in data["charts"]:
        missing = required - chart.keys()
        assert not missing, f"Chart '{chart.get('chart_id')}' missing fields: {missing}"


def test_get_charts_data_is_list(api_client):
    data = api_client.get("/charts").json()
    for chart in data["charts"]:
        assert isinstance(chart["data"], list), f"data field must be a list, got {type(chart['data'])}"


def test_get_charts_chart_id_is_string(api_client):
    data = api_client.get("/charts").json()
    for chart in data["charts"]:
        assert isinstance(chart["chart_id"], str)


# ── GET /charts/{chart_id} ────────────────────────────────────────────────────

@pytest.mark.parametrize("chart_id", CHART_IDS)
def test_get_single_chart_returns_200(api_client, chart_id):
    response = api_client.get(f"/charts/{chart_id}")
    assert response.status_code == 200


@pytest.mark.parametrize("chart_id", CHART_IDS)
def test_get_single_chart_returns_correct_id(api_client, chart_id):
    data = api_client.get(f"/charts/{chart_id}").json()
    assert data["chart_id"] == chart_id


def test_get_unknown_chart_returns_404(api_client):
    response = api_client.get("/charts/nonexistent_chart")
    assert response.status_code == 404


# ── POST /chat ────────────────────────────────────────────────────────────────

def test_post_chat_returns_200(api_client):
    response = api_client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 200


def test_post_chat_response_has_required_keys(api_client):
    data = api_client.post("/chat", json={"message": "Hello"}).json()
    assert "reply" in data
    assert "chart" in data
    assert "intent" in data


def test_post_chat_reply_is_string(api_client):
    data = api_client.post("/chat", json={"message": "Hello"}).json()
    assert isinstance(data["reply"], str)
    assert len(data["reply"]) > 0


def test_post_chat_accepts_chart_id(api_client):
    response = api_client.post(
        "/chat",
        json={"message": "Explain this", "chart_id": "contraceptive_prevalence"}
    )
    assert response.status_code == 200


def test_post_chat_accepts_null_chart_id(api_client):
    response = api_client.post(
        "/chat",
        json={"message": "What is HIV prevalence in Rwanda?", "chart_id": None}
    )
    assert response.status_code == 200
