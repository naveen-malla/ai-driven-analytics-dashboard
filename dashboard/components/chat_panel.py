"""
chat_panel.py — The AI chat interface for asking questions about health data.

Usage:
    from dashboard.components.chat_panel import render_chat_panel

    render_chat_panel(selected_chart_id="contraceptive_prevalence")

The chat panel sends the user's question to the AI backend and displays
the response. If the AI generates a new chart in response to a question,
that chart is shown inline inside the conversation.

The conversation history is stored in Streamlit session state so it
persists while the user is on the page (but resets on page refresh).
"""

import streamlit as st

# Import the function that sends messages to the AI backend
from dashboard.api_client import send_chat_message

# Import design tokens for consistent visual styling
from dashboard.theme import PRIMARY_COLOR, ACCENT_COLOR, TEXT_MUTED

# Import the chart renderer so we can show AI-generated charts inline
from dashboard.components.chart_card import render_chart_card


def render_chat_panel(selected_chart_id: str | None = None):
    """
    Renders the full AI chat panel — message history plus input box.

    Parameters:
        selected_chart_id — if a chart card was clicked, pass its ID here.
                            The AI will use this as context for the conversation.
                            Pass None if no chart is selected (general question mode).
    """

    # ── Section Header ─────────────────────────────────────────────────────────
    st.markdown("---")  # horizontal divider to separate charts from chat
    st.subheader("Ask the data")

    # Show a context label when the user has selected a specific chart
    if selected_chart_id:
        # Make the chart ID human-readable by replacing underscores with spaces
        readable_chart_name = selected_chart_id.replace("_", " ").title()
        st.caption(
            f"Asking about: **{readable_chart_name}**. "
            "Click another chart to switch context, or ask a general question below."
        )
    else:
        st.caption(
            "Ask any question about health indicators across Rwanda, Kenya, Uganda, Ethiopia, and Tanzania."
        )

    # ── Chat History Display ───────────────────────────────────────────────────
    # st.session_state.chat_history is a list of message dicts:
    # [
    #   {"role": "user",      "content": "What is the HIV rate in Rwanda?", "chart": None},
    #   {"role": "assistant", "content": "Rwanda's HIV prevalence...",       "chart": None},
    # ]
    #
    # We loop through the list and display each message with st.chat_message(),
    # which renders a speech-bubble-style UI for each turn.

    chat_history = st.session_state.get("chat_history", [])

    for message in chat_history:
        role = message.get("role", "user")         # "user" or "assistant"
        content = message.get("content", "")       # the text of the message
        attached_chart = message.get("chart", None) # optional chart object

        # st.chat_message() creates a styled message bubble with an avatar icon
        with st.chat_message(role):
            st.markdown(content)

            # If the AI response included a generated chart, show it here inline
            if attached_chart:
                render_chart_card(attached_chart, is_selected=False)

    # ── Chat Input Box ─────────────────────────────────────────────────────────
    # st.chat_input() renders a text box pinned to the bottom of the container.
    # It returns the user's typed text when they press Enter, or None otherwise.
    placeholder_text = (
        f"Ask about {selected_chart_id.replace('_', ' ')} across countries..."
        if selected_chart_id
        else "Ask about any health indicator across these five countries..."
    )

    user_question = st.chat_input(placeholder=placeholder_text)

    # If the user typed something and pressed Enter, process their question
    if user_question:
        _handle_user_message(user_question, selected_chart_id)


def _handle_user_message(user_question: str, chart_id: str | None):
    """
    Processes a user's question: saves it to history, sends it to the AI,
    then saves the AI's response to history and refreshes the page.

    This is a private helper function (underscore prefix = not called from outside).

    Parameters:
        user_question — the text the user typed
        chart_id      — the currently selected chart ID, or None
    """

    # ── Add User Message to History ───────────────────────────────────────────
    # First, record what the user asked in the chat history
    user_message = {
        "role": "user",
        "content": user_question,
        "chart": None,    # user messages never contain charts
    }
    st.session_state.chat_history.append(user_message)

    # ── Send to AI and Get Response ───────────────────────────────────────────
    # Show a spinner while waiting for the AI — it can take a few seconds
    with st.spinner("Thinking..."):
        ai_response = send_chat_message(
            message=user_question,
            chart_id=chart_id,
        )

    # ── Extract the AI Response Parts ────────────────────────────────────────
    # The response dict has three keys (per Contract 4):
    #   "reply"  — the text explanation from the AI
    #   "chart"  — a chart object if the AI generated one, or None
    #   "intent" — what type of response this is (informational, for debugging)
    reply_text = ai_response.get("reply", "No response from AI.")
    generated_chart = ai_response.get("chart", None)

    # ── Add AI Response to History ────────────────────────────────────────────
    assistant_message = {
        "role": "assistant",
        "content": reply_text,
        "chart": generated_chart,   # None for most replies, a chart dict for new_analysis
    }
    st.session_state.chat_history.append(assistant_message)

    # ── Refresh the Page ──────────────────────────────────────────────────────
    # st.rerun() forces Streamlit to re-render the page from the top so the new
    # messages appear in the chat history display above.
    st.rerun()
