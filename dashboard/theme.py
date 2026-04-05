"""
theme.py — Design token constants for the Health Insights Dashboard.

This file is the single source of truth for all colors, sizes, and visual
settings used in chart rendering. Change a value here and it changes across
every chart in the dashboard.

These constants are used in:
- dashboard/components/chart_card.py  (chart colors, sizes)
- dashboard/app.py                    (page-level colors via CSS overrides)

Design system source: ui-ux-pro-max Analytics Dashboard palette (row 8).
Typography: Minimal Swiss pairing — Inter, all weights.
"""

# ── Primary Color Palette ──────────────────────────────────────────────────────
# These colors come from the Analytics Dashboard palette in the design system.

# Primary brand color — deep blue. Used for primary chart bars, buttons,
# selected highlights, and interactive elements.
PRIMARY_COLOR = "#1E40AF"

# Secondary blue — lighter than primary. Used for secondary data series,
# hover states, and supporting visual elements.
SECONDARY_COLOR = "#3B82F6"

# Amber — the accent/highlight color. Used to call out the metric that needs
# the most attention, and for chart highlights when comparing across countries.
ACCENT_COLOR = "#F59E0B"

# Near-white slate — main page background.
PAGE_BACKGROUND = "#F8FAFC"

# Light blue-tinted — sidebar and card backgrounds.
SIDEBAR_BACKGROUND = "#EFF6FF"

# Dark navy — primary text color for headings and chart labels.
TEXT_COLOR = "#1E3A8A"

# Medium slate — secondary/muted text for subtitles and axis labels.
TEXT_MUTED = "#475569"

# Light slate — border color for cards and dividers.
BORDER_COLOR = "#DBEAFE"

# ── Chart Color Sequence ───────────────────────────────────────────────────────
# When multiple countries appear in a single chart, cycle through these colors.
# The sequence is designed so neighboring bars are clearly distinct even in
# black-and-white print or for colorblind viewers (blue/amber/teal/slate family).
CHART_COLORS = [
    "#1E40AF",  # deep blue      — primary series / Rwanda
    "#F59E0B",  # amber          — second series / Kenya
    "#0891B2",  # cyan           — third series / Uganda
    "#059669",  # teal-green     — fourth series / Ethiopia
    "#7C3AED",  # violet         — fifth series / Tanzania
]

# ── Chart for "Lower = Better" Indicators ─────────────────────────────────────
# maternal_mortality and under5_mortality use a warm color scale to signal
# that higher bars are negative outcomes, not positive ones.
CHART_COLORS_LOWER_BETTER = [
    "#EF4444",  # red     — worst performing country (highest mortality)
    "#F97316",  # orange
    "#F59E0B",  # amber
    "#84CC16",  # lime
    "#22C55E",  # green   — best performing country (lowest mortality)
]

# ── Grid and Background Colors for Charts ─────────────────────────────────────
# Chart plot background — matches the main page background.
CHART_PLOT_BACKGROUND = "#F8FAFC"

# Gridline color — subtle so gridlines don't compete with the data.
CHART_GRID_COLOR = "#E2E8F0"

# ── Chart Sizing ───────────────────────────────────────────────────────────────
# Default chart height in pixels. 350px fits 6 charts in 3 rows without
# excessive vertical scrolling on a standard 1440×900 laptop display.
CHART_HEIGHT = 350

# ── Typography Sizes ───────────────────────────────────────────────────────────
# Font size for chart axis tick labels (country names, numeric values).
AXIS_FONT_SIZE = 12

# Font size for axis titles (e.g. "Country", "Prevalence (%)").
AXIS_TITLE_FONT_SIZE = 13

# Font size for chart titles shown inside the Plotly figure.
# Note: the card heading is rendered by Streamlit, not Plotly, so this only
# applies if a title is embedded in the figure itself.
TITLE_FONT_SIZE = 15

# ── Bar Chart Settings ─────────────────────────────────────────────────────────
# Opacity for bar fills — slightly transparent so gridlines remain visible
# behind bars when bars overlap (grouped charts).
BAR_OPACITY = 0.85

# Corner radius on bars — 0 = square corners (more professional/data-dense look).
BAR_CORNER_RADIUS = 3

# ── Hover Template ─────────────────────────────────────────────────────────────
# Plotly hover text format. %{x} = x-axis value, %{y:.1f} = y-axis value
# rounded to 1 decimal place, <extra></extra> removes the trace name box.
HOVER_TEMPLATE = "%{x}: <b>%{y:.1f}</b><extra></extra>"
