from __future__ import annotations

from unittest.mock import patch

from closeloop.logging_layer import WorkflowExecutionResult
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


def test_orchestrator_executes_sequential_pipeline() -> None:
    """Test that orchestrator executes agents in sequence and returns structured result."""
    state = create_initial_state("Acme Corp")

    # Mock each agent to avoid requiring API calls
    with patch("closeloop.orchestrator.run_research_agent") as mock_research, \
         patch("closeloop.orchestrator.run_outreach_agent") as mock_outreach, \
         patch("closeloop.orchestrator.run_monitoring_module") as mock_monitoring, \
         patch("closeloop.orchestrator.run_risk_detection_agent") as mock_risk, \
         patch("closeloop.orchestrator.run_recovery_agent") as mock_recovery:

        # Configure mocks to return updated state
        def update_state_research(s: SalesWorkflowState) -> SalesWorkflowState:
            s["industry"] = "Technology"
            s["company_stage"] = "Series B"
            s["persona"] = "VP of Engineering"
            s["pain_points"] = ["scaling infrastructure", "team hiring"]
            return s

        def update_state_outreach(s: SalesWorkflowState) -> SalesWorkflowState:
            s["initial_email"] = "Dear VP, we help with scaling."
            s["last_email"] = "Dear VP, we help with scaling."
            return s

        def update_state_monitoring(s: SalesWorkflowState) -> SalesWorkflowState:
            s["last_contact_days"] = 10
            s["engagement_status"] = "NO_RESPONSE"
            return s

        def update_state_risk(s: SalesWorkflowState) -> SalesWorkflowState:
            s["risk_level"] = "HIGH"
            s["risk_reason"] = "No response after 10 days"
            return s

        def update_state_recovery(s: SalesWorkflowState) -> SalesWorkflowState:
            s["recovery_strategy"] = "Send urgent follow-up"
            s["last_email"] = "Dear VP, urgent follow-up on scaling."
            return s

        mock_research.side_effect = update_state_research
        mock_outreach.side_effect = update_state_outreach
        mock_monitoring.side_effect = update_state_monitoring
        mock_risk.side_effect = update_state_risk
        mock_recovery.side_effect = update_state_recovery

        # Execute orchestrator
        result: WorkflowExecutionResult = run_sales_workflow(state)

        # Assert result structure
        assert "final_state" in result
        assert "logs" in result
        assert isinstance(result["final_state"], dict)
        assert isinstance(result["logs"], list)

        # Assert logs are non-empty and contain all agents
        assert len(result["logs"]) == 5
        agent_names = [log["agent_name"] for log in result["logs"]]
        assert agent_names == [
            "research_agent",
            "outreach_agent",
            "monitoring_module",
            "risk_detection_agent",
            "recovery_agent",
        ]

        # Assert each log entry has required keys
        for log in result["logs"]:
            assert "agent_name" in log
            assert "input_summary" in log
            assert "output_summary" in log
            assert "reasoning" in log

        # Assert final state contains expected fields
        final_state = result["final_state"]
        expected_fields = {
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
        assert expected_fields.issubset(set(final_state.keys()))

        # Assert field values flow through correctly
        assert final_state["industry"] == "Technology"
        assert final_state["risk_level"] == "HIGH"
        assert final_state["recovery_strategy"] == "Send urgent follow-up"
