from __future__ import annotations

from closeloop.state import SalesWorkflowState


def run_monitoring_module(state: SalesWorkflowState) -> SalesWorkflowState:
    """Apply deterministic inactivity simulation without using an LLM."""
    state["last_contact_days"] = 10
    state["engagement_status"] = "NO_RESPONSE"
    return state
