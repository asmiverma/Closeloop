from __future__ import annotations

from closeloop.orchestrator import run_sales_workflow
from closeloop.state import SalesWorkflowState, create_initial_state


def test_state_initialization_has_required_keys() -> None:
    state: SalesWorkflowState = create_initial_state("Acme Corp")

    expected_keys = {
        "company_name",
        "industry",
        "company_stage",
        "persona",
        "pain_points",
        "initial_email",
        "last_email",
        "last_contact_days",
        "engagement_status",
        "risk_level",
        "risk_reason",
        "recovery_strategy",
    }

    assert set(state.keys()) == expected_keys
    assert state["company_name"] == "Acme Corp"


def test_orchestrator_signature_is_callable() -> None:
    state = create_initial_state("Acme Corp")

    try:
        run_sales_workflow(state)
    except NotImplementedError:
        assert True
    else:
        raise AssertionError("Phase 1 orchestrator should be a stub.")
