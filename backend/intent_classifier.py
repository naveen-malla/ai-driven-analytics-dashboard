from __future__ import annotations

from backend.models import IntentResult


def classify_intent(message: str, chart_id: str | None = None) -> IntentResult:
    """Classify the intent of an incoming chat message.

    Stub implementation — Phase 3 will replace this with a Claude API call
    using structured output to return a typed IntentResult.

    Args:
        message: The user's chat message.
        chart_id: Optional chart_id if the user is asking about a specific chart.

    Returns:
        IntentResult with intent, chart_id, and reasoning.
    """
    return IntentResult(
        intent="new_analysis",
        chart_id=None,
        reasoning="Stub — Phase 3 implementation pending",
    )
