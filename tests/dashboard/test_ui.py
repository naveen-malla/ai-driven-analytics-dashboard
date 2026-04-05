"""
Playwright UI tests for the Streamlit dashboard.

Prerequisites — both servers must be running:
    make backend    # FastAPI on :8000
    make dashboard  # Streamlit on :8501

Run:
    PYTHONPATH=. pytest tests/dashboard/test_ui.py -v

These tests verify Marco's UI contract: 6 charts render, each has an
"Ask about this chart" button, chat panel is present and accepts input.
"""

import pytest
from playwright.sync_api import Page, expect

DASHBOARD_URL = "http://localhost:8501"

# Streamlit can take a moment to fully load — this timeout covers it
PAGE_LOAD_TIMEOUT = 15_000  # ms


@pytest.fixture(scope="module")
def page_loaded(browser):
    """Open the dashboard and wait for it to finish loading."""
    page = browser.new_page()
    page.goto(DASHBOARD_URL, timeout=PAGE_LOAD_TIMEOUT)
    # Wait for Streamlit to finish rendering (the main content div appears)
    page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=PAGE_LOAD_TIMEOUT)
    yield page
    page.close()


def test_page_title(page_loaded):
    """Page title should contain 'Health Insights'."""
    expect(page_loaded).to_have_title(lambda t: "Health Insights" in t or "health" in t.lower())


def test_main_heading_visible(page_loaded):
    """Main h1 heading should be visible on the page."""
    heading = page_loaded.locator("h1").first
    expect(heading).to_be_visible()


def test_six_plotly_charts_render(page_loaded):
    """All 6 Plotly chart canvases must be present in the DOM."""
    charts = page_loaded.locator('[class*="js-plotly-plot"]')
    expect(charts).to_have_count(6)


def test_ask_about_buttons_present(page_loaded):
    """Each chart card must have an 'Ask about this chart' button."""
    buttons = page_loaded.locator('button:has-text("Ask about this chart")')
    expect(buttons).to_have_count(6)


def test_chat_input_present(page_loaded):
    """The chat input box must be present."""
    chat_input = page_loaded.locator('[data-testid="stChatInput"]')
    expect(chat_input).to_be_visible()


def test_sidebar_visible(page_loaded):
    """Sidebar with indicator definitions must be present."""
    sidebar = page_loaded.locator('[data-testid="stSidebar"]')
    expect(sidebar).to_be_visible()


def test_click_ask_selects_chart(page_loaded):
    """Clicking 'Ask about this chart' on first chart should highlight it."""
    first_button = page_loaded.locator('button:has-text("Ask about this chart")').first
    first_button.click()
    # After click, the button text changes to "Currently selected"
    selected = page_loaded.locator('button:has-text("Currently selected")')
    expect(selected).to_have_count(1)


def test_chat_input_accepts_text(page_loaded):
    """Typing in the chat input should work without errors."""
    chat_input = page_loaded.locator('[data-testid="stChatInput"] textarea')
    chat_input.fill("What is the contraceptive prevalence in Rwanda?")
    # Verify text was entered (don't submit — stub backend returns placeholder)
    expect(chat_input).to_have_value("What is the contraceptive prevalence in Rwanda?")
