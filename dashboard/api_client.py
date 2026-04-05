"""
api_client.py — Connects the dashboard to the FastAPI backend.

Usage:
    from dashboard.api_client import get_all_charts, get_chart_by_id, send_chat_message

The backend runs at http://localhost:8000. Change BACKEND_URL below if needed.

This file defines three functions:
- get_all_charts()         → ask the backend for all 6 pre-built charts
- get_chart_by_id(id)      → ask for a single chart by its string ID
- send_chat_message(...)   → send a user's question to the AI chat assistant

All functions handle connection errors gracefully — they return empty/fallback
values and print a warning instead of crashing the whole dashboard.
"""

import httpx  # httpx is a modern HTTP library, similar to 'requests' but better for Python 3.12+


# ── Backend Connection Settings ───────────────────────────────────────────────

# The URL where the FastAPI backend is running. This is the only place in the
# dashboard codebase that stores the backend URL (per Contract 5).
BACKEND_URL = "http://localhost:8000"

# How long to wait for the backend to respond before giving up, in seconds.
# 30 seconds is generous — if the backend is running locally it should respond
# in under 2 seconds, but DuckDB queries can take a moment on first run.
REQUEST_TIMEOUT = 30


# ── Public Functions ───────────────────────────────────────────────────────────

def get_all_charts() -> list[dict]:
    """
    Ask the backend for all 6 pre-built health indicator charts.

    Calls: GET /charts

    Returns a list of chart objects. Each chart object looks like:
        {
            "chart_id": "contraceptive_prevalence",
            "title": "Contraceptive Prevalence Rate by Country",
            "chart_type": "bar",
            "x_key": "country_name",
            "y_key": "value",
            "data": [{"country_name": "Rwanda", "value": 64.2}, ...],
            "x_label": "Country",
            "y_label": "Prevalence (%)",
            "metric_definition": "% of women aged 15-49 using any contraceptive method"
        }

    Returns an empty list [] if the backend is not available or returns an error.
    """
    try:
        # Build the full URL for the /charts endpoint
        charts_url = BACKEND_URL + "/charts"

        # Make the HTTP GET request to the backend
        response = httpx.get(charts_url, timeout=REQUEST_TIMEOUT)

        # Raise an error if the backend returned a non-200 status code (e.g. 500)
        response.raise_for_status()

        # Parse the JSON response body
        response_data = response.json()

        # The backend wraps the list in a "charts" key (per Contract 1)
        charts_list = response_data.get("charts", [])

        return charts_list

    except httpx.ConnectError:
        # This happens when the backend server is not running at all
        print(f"WARNING: Cannot connect to backend at {BACKEND_URL}. Is the FastAPI server running?")
        return []

    except httpx.TimeoutException:
        # This happens when the backend takes too long to respond
        print(f"WARNING: Backend at {BACKEND_URL} timed out after {REQUEST_TIMEOUT}s.")
        return []

    except Exception as unexpected_error:
        # Catch any other unexpected problem so the dashboard does not crash
        print(f"WARNING: Unexpected error fetching charts: {unexpected_error}")
        return []


def get_chart_by_id(chart_id: str) -> dict | None:
    """
    Ask the backend for a single chart by its string ID.

    Calls: GET /charts/{chart_id}

    Valid chart IDs (from Contract 2):
        "contraceptive_prevalence", "maternal_mortality", "antenatal_care",
        "skilled_birth", "under5_mortality", "hiv_prevalence"

    Returns:
        A single chart dict (same shape as the items in get_all_charts()),
        or None if the chart was not found or the backend is unavailable.
    """
    try:
        # Build the URL for the specific chart endpoint
        single_chart_url = BACKEND_URL + "/charts/" + chart_id

        # Make the HTTP GET request
        response = httpx.get(single_chart_url, timeout=REQUEST_TIMEOUT)

        # If the backend returns 404 (not found), return None gracefully
        if response.status_code == 404:
            print(f"WARNING: Chart '{chart_id}' not found in backend.")
            return None

        # Raise an error for any other bad status code
        response.raise_for_status()

        # Return the chart object directly (not wrapped in a list)
        chart_data = response.json()
        return chart_data

    except httpx.ConnectError:
        print(f"WARNING: Cannot connect to backend at {BACKEND_URL}. Is the FastAPI server running?")
        return None

    except httpx.TimeoutException:
        print(f"WARNING: Backend at {BACKEND_URL} timed out after {REQUEST_TIMEOUT}s.")
        return None

    except Exception as unexpected_error:
        print(f"WARNING: Unexpected error fetching chart '{chart_id}': {unexpected_error}")
        return None


def send_chat_message(message: str, chart_id: str | None = None) -> dict:
    """
    Send a question to the AI chat assistant and get a response.

    Calls: POST /chat

    Parameters:
        message   — the user's question in plain English
                    e.g. "What is the contraceptive prevalence in Rwanda?"
        chart_id  — if the user is asking about a specific chart, pass its ID here
                    (e.g. "contraceptive_prevalence"). Pass None for general questions.

    Returns a dict with three keys (per Contract 4):
        {
            "reply":  "Plain English explanation from the AI",
            "chart":  null   OR a full chart object (when intent = "new_analysis"),
            "intent": "explain_chart" | "new_analysis" | "reject"
        }

    Returns a safe fallback dict if the backend is unavailable, so the UI never crashes.
    """
    # Build the request body as a Python dict (httpx will convert it to JSON)
    request_body = {
        "message": message,
        "chart_id": chart_id,   # None is sent as JSON null, which is correct per Contract 4
    }

    # This is the fallback response returned when something goes wrong.
    # The UI should display this message to the user instead of crashing.
    fallback_response = {
        "reply": "Sorry, the AI assistant is not available right now. Please check that the backend server is running.",
        "chart": None,
        "intent": "reject",
    }

    try:
        # Build the URL for the chat endpoint
        chat_url = BACKEND_URL + "/chat"

        # Make the HTTP POST request, sending the body as JSON
        response = httpx.post(chat_url, json=request_body, timeout=REQUEST_TIMEOUT)

        # Raise an error if the backend returned a non-200 status code
        response.raise_for_status()

        # Parse and return the AI response
        ai_response = response.json()
        return ai_response

    except httpx.ConnectError:
        print(f"WARNING: Cannot connect to backend at {BACKEND_URL}. Is the FastAPI server running?")
        return fallback_response

    except httpx.TimeoutException:
        # Chat requests can legitimately take longer (the AI must think), but
        # 30 seconds is still too long to wait silently
        print(f"WARNING: Chat request to backend timed out after {REQUEST_TIMEOUT}s.")
        fallback_response["reply"] = "The AI assistant took too long to respond. Please try again."
        return fallback_response

    except Exception as unexpected_error:
        print(f"WARNING: Unexpected error sending chat message: {unexpected_error}")
        return fallback_response
