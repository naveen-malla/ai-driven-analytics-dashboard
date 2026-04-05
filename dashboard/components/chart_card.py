"""
chart_card.py — Renders a single chart from the backend chart spec.

Usage:
    from dashboard.components.chart_card import render_chart_card

    was_clicked = render_chart_card(chart_spec, is_selected=False)
    if was_clicked:
        st.session_state.selected_chart_id = chart_spec["chart_id"]

A "chart spec" is a dict returned by the backend. It looks like:
    {
        "chart_id":          "contraceptive_prevalence",
        "title":             "Contraceptive Prevalence Rate by Country",
        "chart_type":        "bar",          # one of: bar, line, area, scatter, pie
        "x_key":             "country_name", # which dict key holds the X-axis values
        "y_key":             "value",        # which dict key holds the Y-axis values
        "data":              [{"country_name": "Rwanda", "value": 64.2}, ...],
        "x_label":           "Country",
        "y_label":           "Prevalence (%)",
        "metric_definition": "% of women aged 15-49 using any contraceptive method"
    }

This module supports bar, line, and area chart types. Scatter and pie fall back
to bar for simplicity — if new chart types are needed, add them here.
"""

import plotly.graph_objects as go
import streamlit as st

# Import design tokens from our central theme file so colors/sizes are consistent
from dashboard.theme import (
    CHART_COLORS,
    CHART_COLORS_LOWER_BETTER,
    CHART_PLOT_BACKGROUND,
    CHART_GRID_COLOR,
    CHART_HEIGHT,
    AXIS_FONT_SIZE,
    AXIS_TITLE_FONT_SIZE,
    TITLE_FONT_SIZE,
    BAR_OPACITY,
    HOVER_TEMPLATE,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    ACCENT_COLOR,
    TEXT_COLOR,
    TEXT_MUTED,
    BORDER_COLOR,
)

# ── Which chart IDs use "lower = better" color coding ─────────────────────────
# For these charts, a HIGH bar is BAD (e.g. high maternal mortality is bad).
# We use a warm (red-to-green) color scale to make that immediately obvious.
LOWER_IS_BETTER_CHARTS = {"maternal_mortality", "under5_mortality", "hiv_prevalence"}


def render_chart_card(chart_spec: dict, is_selected: bool = False) -> bool:
    """
    Renders a chart card inside a Streamlit container.

    The card contains:
    - A title (from chart_spec["title"])
    - A Plotly chart (type determined by chart_spec["chart_type"])
    - A metric definition tooltip/caption
    - An "Ask about this chart" button

    Parameters:
        chart_spec   — the chart object dict from the backend API
        is_selected  — if True, show a highlighted border around the card to
                       indicate this is the chart the user last clicked on

    Returns:
        True  — if the user clicked the "Ask about this chart" button
        False — otherwise
    """
    chart_id = chart_spec.get("chart_id", "unknown")
    chart_title = chart_spec.get("title", "Chart")
    chart_data = chart_spec.get("data", [])

    # Determine whether to use the warm color scale (for "lower = better" metrics)
    use_warm_colors = chart_id in LOWER_IS_BETTER_CHARTS

    # ── Card Container ─────────────────────────────────────────────────────────
    # We use a Streamlit container to group the title + chart + button together.
    # The border color changes to highlight the selected chart.
    border_style = f"2px solid {ACCENT_COLOR}" if is_selected else f"1px solid {BORDER_COLOR}"

    # Inject a small CSS block to style this specific card.
    # We use a unique key based on chart_id so multiple cards don't interfere.
    st.markdown(
        f"""
        <div id="card-{chart_id}" style="
            border: {border_style};
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 8px;
            background-color: #FFFFFF;
        ">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Build the Plotly Figure ────────────────────────────────────────────────
    chart_figure = _build_chart(chart_spec, use_warm_colors)

    # ── Display the Chart ──────────────────────────────────────────────────────
    # use_container_width=True makes the chart fill the column it's placed in
    st.plotly_chart(chart_figure, use_container_width=True, key=f"chart_{chart_id}")

    # ── Metric Definition Caption ──────────────────────────────────────────────
    # Show the metric definition as small grey text below the chart.
    # This helps non-expert viewers understand what they are looking at.
    metric_definition = chart_spec.get("metric_definition", "")
    if metric_definition:
        st.caption(f"Definition: {metric_definition}")

    # ── "Ask about this chart" Button ─────────────────────────────────────────
    # Each chart card has its own button. The button key must be unique per chart
    # (Streamlit requires unique widget keys on the same page).
    button_label = "Ask about this chart" if not is_selected else "Currently selected"
    button_was_clicked = st.button(
        label=button_label,
        key=f"ask_button_{chart_id}",
        disabled=is_selected,       # disable the button if this chart is already selected
        use_container_width=True,
    )

    # Return True if the user just clicked the button; False otherwise
    return button_was_clicked


def _build_chart(chart_spec: dict, use_warm_colors: bool) -> go.Figure:
    """
    Builds and returns a Plotly Figure based on the chart spec.

    This is a private helper function (indicated by the underscore prefix).
    It is only called from render_chart_card() above.

    Parameters:
        chart_spec      — the full chart dict from the backend
        use_warm_colors — if True, use red/amber/green colors (lower = better)

    Returns:
        A Plotly go.Figure object ready to be displayed with st.plotly_chart()
    """
    chart_type = chart_spec.get("chart_type", "bar")
    chart_data = chart_spec.get("data", [])
    x_key = chart_spec.get("x_key", "country_name")   # which column is the X axis
    y_key = chart_spec.get("y_key", "value")           # which column is the Y axis
    x_label = chart_spec.get("x_label", "")
    y_label = chart_spec.get("y_label", "")

    # If the backend returned no data rows, show a friendly empty-state message
    if not chart_data:
        return _build_empty_chart(chart_spec.get("title", "No data available"))

    # Extract the X-axis values (e.g. country names) from the data rows
    x_values = [row.get(x_key, "") for row in chart_data]

    # Extract the Y-axis values (e.g. numeric indicators) from the data rows
    y_values = [row.get(y_key, 0) for row in chart_data]

    # ── Assign a Bar Color Per Country (or data point) ─────────────────────────
    # For bar charts with warm colors: sort by value so the color carries meaning
    # (red = highest = worst for "lower is better" metrics)
    if use_warm_colors and chart_type == "bar":
        bar_colors = _assign_warm_colors(y_values)
    else:
        # Default: cycle through our standard blue/amber/teal palette
        bar_colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(x_values))]

    # ── Build the Figure Based on Chart Type ──────────────────────────────────
    if chart_type == "bar":
        figure = _build_bar_chart(x_values, y_values, bar_colors, x_label, y_label)

    elif chart_type == "line":
        figure = _build_line_chart(x_values, y_values, x_label, y_label)

    elif chart_type == "area":
        figure = _build_area_chart(x_values, y_values, x_label, y_label)

    else:
        # Fallback: unsupported chart types render as bars
        # (scatter and pie not currently needed for this dashboard)
        figure = _build_bar_chart(x_values, y_values, bar_colors, x_label, y_label)

    # ── Apply Consistent Layout Styling ───────────────────────────────────────
    figure.update_layout(
        height=CHART_HEIGHT,
        plot_bgcolor=CHART_PLOT_BACKGROUND,   # background color of the chart area
        paper_bgcolor="rgba(0,0,0,0)",        # transparent outer background (inherits from card)
        font=dict(
            family="Inter, sans-serif",
            size=AXIS_FONT_SIZE,
            color=TEXT_COLOR,
        ),
        margin=dict(l=10, r=10, t=20, b=10),  # tight margins so chart fills its card
        showlegend=False,                      # no legend needed (country names are on the axis)
        xaxis=dict(
            title=dict(text=x_label, font=dict(size=AXIS_TITLE_FONT_SIZE, color=TEXT_MUTED)),
            gridcolor=CHART_GRID_COLOR,
            linecolor=CHART_GRID_COLOR,
            tickfont=dict(size=AXIS_FONT_SIZE),
        ),
        yaxis=dict(
            title=dict(text=y_label, font=dict(size=AXIS_TITLE_FONT_SIZE, color=TEXT_MUTED)),
            gridcolor=CHART_GRID_COLOR,
            linecolor=CHART_GRID_COLOR,
            tickfont=dict(size=AXIS_FONT_SIZE),
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=AXIS_FONT_SIZE,
            font_family="Inter, sans-serif",
        ),
    )

    return figure


def _build_bar_chart(
    x_values: list,
    y_values: list,
    bar_colors: list,
    x_label: str,
    y_label: str,
) -> go.Figure:
    """
    Builds a vertical bar chart with one bar per country.

    Parameters:
        x_values   — list of category labels (e.g. country names)
        y_values   — list of numeric values (e.g. prevalence percentages)
        bar_colors — list of hex color strings, one per bar
        x_label    — label for the X axis
        y_label    — label for the Y axis

    Returns a Plotly Figure.
    """
    figure = go.Figure()

    # Add a single Bar trace to the figure.
    # Each bar gets its own color from bar_colors.
    figure.add_trace(
        go.Bar(
            x=x_values,
            y=y_values,
            marker=dict(
                color=bar_colors,
                opacity=BAR_OPACITY,
                line=dict(width=0),   # no border on bars — cleaner look
            ),
            hovertemplate=HOVER_TEMPLATE,
        )
    )

    return figure


def _build_line_chart(
    x_values: list,
    y_values: list,
    x_label: str,
    y_label: str,
) -> go.Figure:
    """
    Builds a line chart — used for time-series data (year on X axis).

    Parameters:
        x_values — list of years or time labels
        y_values — list of numeric values
        x_label  — label for the X axis
        y_label  — label for the Y axis

    Returns a Plotly Figure.
    """
    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines+markers",   # show both the line and individual point markers
            line=dict(
                color=PRIMARY_COLOR,
                width=2,
            ),
            marker=dict(
                color=PRIMARY_COLOR,
                size=6,
            ),
            hovertemplate=HOVER_TEMPLATE,
        )
    )

    return figure


def _build_area_chart(
    x_values: list,
    y_values: list,
    x_label: str,
    y_label: str,
) -> go.Figure:
    """
    Builds an area chart (line chart with shaded fill below the line).
    Useful for showing cumulative or coverage metrics over time.

    Parameters:
        x_values — list of time labels or categories
        y_values — list of numeric values
        x_label  — label for the X axis
        y_label  — label for the Y axis

    Returns a Plotly Figure.
    """
    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            fill="tozeroy",                    # shade from the line down to y=0
            line=dict(color=PRIMARY_COLOR, width=2),
            fillcolor=SECONDARY_COLOR + "33",  # "33" at the end = 20% opacity hex
            hovertemplate=HOVER_TEMPLATE,
        )
    )

    return figure


def _build_empty_chart(title: str) -> go.Figure:
    """
    Returns a placeholder figure when the backend returned no data rows.

    This happens if the DuckDB query returned an empty result — for example,
    if the data pipeline has not been run yet. The empty chart shows a message
    instead of a blank white box, which would look broken.

    Parameters:
        title — the chart title to show in the annotation

    Returns a Plotly Figure with an annotation explaining there is no data.
    """
    figure = go.Figure()

    # Add a text annotation in the centre of the empty chart area
    figure.add_annotation(
        text="No data available — backend may still be loading",
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=13, color=TEXT_MUTED),
    )

    figure.update_layout(
        height=CHART_HEIGHT,
        plot_bgcolor=CHART_PLOT_BACKGROUND,
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=20, b=10),
    )

    return figure


def _assign_warm_colors(y_values: list) -> list:
    """
    Assigns colors from CHART_COLORS_LOWER_BETTER based on rank.

    The country with the HIGHEST value (worst outcome for "lower = better"
    metrics) gets the red color. The lowest gets green.

    Parameters:
        y_values — list of numeric values, one per data point

    Returns:
        A list of hex color strings, one per data point, in the same order
        as y_values (i.e. NOT sorted — the colors match the original order).
    """
    number_of_countries = len(y_values)

    if number_of_countries == 0:
        return []

    # Create a sorted version of the values to determine rank
    sorted_values = sorted(y_values, reverse=True)  # highest first = worst first = red

    # Build a mapping: value → color (based on rank in the sorted list)
    value_to_color = {}
    for rank, value in enumerate(sorted_values):
        # Map rank 0 (worst) → red, rank (n-1) (best) → green
        # We cap the color index at the length of CHART_COLORS_LOWER_BETTER
        color_index = min(rank, len(CHART_COLORS_LOWER_BETTER) - 1)
        value_to_color[value] = CHART_COLORS_LOWER_BETTER[color_index]

    # Return colors in the original y_values order so they match the bars
    assigned_colors = [value_to_color.get(value, CHART_COLORS_LOWER_BETTER[0]) for value in y_values]
    return assigned_colors
