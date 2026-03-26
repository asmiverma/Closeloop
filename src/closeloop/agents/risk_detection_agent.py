from __future__ import annotations

from closeloop.state import SalesWorkflowState


def run_risk_detection_agent(state: SalesWorkflowState) -> SalesWorkflowState:
    """Classify risk deterministically from inactivity and engagement status."""
    days = int(state.get("last_contact_days", 0))
    status = str(state.get("engagement_status", "")).strip().upper()

    if status == "NO_RESPONSE" and days > 7:
        state["risk_level"] = "HIGH"
        state["risk_reason"] = f"No response after {days} days"
    elif status == "NO_RESPONSE" and days >= 3:
        state["risk_level"] = "MEDIUM"
        state["risk_reason"] = f"No response for {days} days"
    else:
        state["risk_level"] = "LOW"
        state["risk_reason"] = "Recent engagement or low inactivity window"

    return state
