def handle_reject(message: str) -> str:
    """Return a refusal message for out-of-scope questions."""
    return (
        "That question is outside what this dashboard can answer. "
        "This system covers WHO Global Health Observatory indicators for Rwanda, Kenya, "
        "Uganda, Ethiopia, and Tanzania. I can answer questions about contraceptive prevalence, "
        "maternal mortality, antenatal care coverage, skilled birth attendance, "
        "under-5 mortality, and HIV prevalence. What would you like to know about these?"
    )
