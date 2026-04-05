from __future__ import annotations

from backend.handlers.explain_chart import handle_explain_chart
from backend.handlers.new_analysis import handle_new_analysis
from backend.handlers.reject import handle_reject
from backend.intent_classifier import classify_intent
from backend.models import ChatResponse


def orchestrate(message: str, chart_id: str | None = None) -> ChatResponse:
    """Route a chat message to the appropriate handler based on intent.

    Stub implementation — Phase 3 will complete the intent-to-handler routing
    with real Claude API integration.

    Args:
        message: The user's chat message.
        chart_id: Optional chart_id if the user is in chart follow-up mode.

    Returns:
        A ChatResponse with the handler's reply, an optional updated chart,
        and the classified intent string.
    """
    intent_result = classify_intent(message, chart_id=chart_id)

    if intent_result.intent == "reject":
        reply = handle_reject(message)
    elif intent_result.intent == "explain_chart":
        reply = handle_explain_chart(message, chart_id=intent_result.chart_id)
    else:
        reply = handle_new_analysis(message)

    return ChatResponse(
        reply=reply,
        chart=None,
        intent=intent_result.intent,
    )
