"""
app.py — Main dashboard application entry point.

Run with:
    streamlit run dashboard/app.py

What this app does:
1. Loads all 6 health indicator charts from the FastAPI backend
2. Displays them in a 2-column grid (3 rows × 2 columns = 6 charts)
3. Lets the user click "Ask about this chart" to select a chart for AI follow-up
4. Shows a full-width AI chat panel below the chart grid

The app talks to the backend at http://localhost:8000 via dashboard/api_client.py.
If the backend is not running, charts will be empty but the app will not crash.

Design brief: dashboard/DESIGN_BRIEF.md
Theme/colors: dashboard/theme.py
"""

import streamlit as st

# Import our custom modules
from dashboard.api_client import get_all_charts
from dashboard.components.chart_card import render_chart_card
from dashboard.components.chat_panel import render_chat_panel
from dashboard import theme  # noqa: F401 — imported so theme constants are accessible if needed


# ── Page Configuration ─────────────────────────────────────────────────────────
# This must be the FIRST Streamlit command in the script.
# layout="wide" uses the full browser width instead of a narrow centered column.
st.set_page_config(
    page_title="Health Insights",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Session State Initialisation ──────────────────────────────────────────────
# Session state variables persist for the duration of the user's browser session.
# We must check if they exist before using them (they don't exist on first load).

# selected_chart_id: the chart the user last clicked "Ask about" for.
# None means no chart is selected — the chat panel accepts general questions.
if "selected_chart_id" not in st.session_state:
    st.session_state.selected_chart_id = None

# chat_history: the full conversation between the user and the AI assistant.
# List of dicts: [{"role": "user"|"assistant", "content": str, "chart": dict|None}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Health Insights")
    st.caption("WHO Global Health Observatory data — Rwanda, Kenya, Uganda, Ethiopia, Tanzania")

    st.markdown("---")
    st.markdown("### About this dashboard")
    st.markdown(
        "This dashboard shows six key health indicators across Kasha's five core markets "
        "in East Africa. The data comes from the WHO Global Health Observatory — the official "
        "source for international public health statistics."
    )

    st.markdown("---")
    st.markdown("### Indicator definitions")

    # Each expander shows the plain-English definition of one indicator.
    # A CXO who needs context can expand it; others can ignore it.
    with st.expander("Contraceptive prevalence"):
        st.markdown(
            "The percentage of women aged 15–49 who are currently using any method of "
            "contraception. A higher percentage means more women have access to and are "
            "using reproductive health choices."
        )

    with st.expander("Maternal mortality ratio"):
        st.markdown(
            "The number of maternal deaths per 100,000 live births. A maternal death is "
            "a death caused by pregnancy or childbirth complications. **Lower is better.**"
        )

    with st.expander("Antenatal care coverage"):
        st.markdown(
            "The percentage of pregnant women who received at least four antenatal care "
            "visits during pregnancy. Regular check-ups reduce complications and improve "
            "outcomes for mother and child."
        )

    with st.expander("Skilled birth attendance"):
        st.markdown(
            "The percentage of births attended by a skilled health worker — a doctor, "
            "nurse, or midwife. Skilled attendance reduces the risk of maternal and "
            "newborn complications during delivery."
        )

    with st.expander("Under-5 mortality rate"):
        st.markdown(
            "The number of deaths among children under five years old per 1,000 live "
            "births. This is a key indicator of overall child health and healthcare "
            "system quality. **Lower is better.**"
        )

    with st.expander("HIV prevalence"):
        st.markdown(
            "The percentage of adults aged 15–49 living with HIV. This indicator "
            "reflects the burden of HIV across the population and informs prevention "
            "and treatment programme priorities. **Lower is better.**"
        )

    st.markdown("---")

    # Button to reset the chat history and chart selection
    if st.button("Clear chat history", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.selected_chart_id = None
        st.rerun()


# ── Main Page ──────────────────────────────────────────────────────────────────

# Page header — concise and informative
st.title("Health Indicators: East Africa")
st.markdown(
    "**Rwanda · Kenya · Uganda · Ethiopia · Tanzania** — latest available WHO data. "
    "Click any chart to ask the AI assistant a follow-up question."
)

st.markdown("---")


# ── Load Chart Data ────────────────────────────────────────────────────────────
# Fetch all 6 charts from the backend. This call is cached by Streamlit so it
# only hits the backend once per session (not on every page re-render).
#
# @st.cache_data tells Streamlit: "remember the result of this function and
# return the same result next time, unless the page was fully refreshed."
@st.cache_data(ttl=300)   # ttl=300 means refresh the cache every 5 minutes
def load_charts() -> list[dict]:
    """
    Fetches all 6 chart specs from the FastAPI backend.
    Returns an empty list if the backend is unavailable.
    Cached for 5 minutes to avoid repeated API calls on every interaction.
    """
    return get_all_charts()


all_charts = load_charts()


# ── Backend Unavailable State ─────────────────────────────────────────────────
# If the backend returned no charts, show a clear warning instead of leaving
# the page blank (which would look broken and confuse the user).
if not all_charts:
    st.warning(
        "The data backend is not available. "
        "Please make sure the FastAPI server is running with: "
        "`uvicorn backend.main:app --reload`"
    )
    # Stop rendering here — don't show the empty chart grid
    st.stop()


# ── Chart Grid ────────────────────────────────────────────────────────────────
# Display all 6 charts in a 2-column grid.
# We use st.columns(2) to create two side-by-side columns.
# Then we loop through the charts, placing them alternately in left and right columns.

st.subheader("Health indicators by country")

# Split the 6 charts into two columns: [0,2,4] go in the left column, [1,3,5] in the right
left_column, right_column = st.columns(2)

for chart_index, chart_spec in enumerate(all_charts):
    chart_id = chart_spec.get("chart_id", f"chart_{chart_index}")

    # Even-indexed charts (0, 2, 4) go in the left column
    # Odd-indexed charts (1, 3, 5) go in the right column
    if chart_index % 2 == 0:
        target_column = left_column
    else:
        target_column = right_column

    # Render the chart card inside its column
    with target_column:
        # Determine if this chart is the currently selected one
        is_this_chart_selected = (st.session_state.selected_chart_id == chart_id)

        # render_chart_card returns True if the user clicked "Ask about this chart"
        user_clicked_ask = render_chart_card(chart_spec, is_selected=is_this_chart_selected)

        # If the user clicked the button on this chart, update the selected chart
        if user_clicked_ask:
            st.session_state.selected_chart_id = chart_id
            # Rerun so the chat panel below updates to reflect the new selection
            st.rerun()


# ── AI Chat Panel ──────────────────────────────────────────────────────────────
# The chat panel appears below the chart grid, full width.
# It receives the currently selected chart ID so the AI knows what context to use.
render_chat_panel(selected_chart_id=st.session_state.selected_chart_id)
