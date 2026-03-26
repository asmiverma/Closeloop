from __future__ import annotations

from closeloop.agents.monitoring_module import run_monitoring_module
from closeloop.agents.outreach_agent import run_outreach_agent
from closeloop.agents.recovery_agent import run_recovery_agent
from closeloop.agents.research_agent import run_research_agent
from closeloop.agents.risk_detection_agent import run_risk_detection_agent
from closeloop.logging_layer import (
    AgentLogEntry,
    WorkflowExecutionResult,
    append_log,
    create_log_entry,
)
from closeloop.state import SalesWorkflowState


def run_sales_workflow(state: SalesWorkflowState) -> WorkflowExecutionResult:
    """Execute the full sequential workflow and return final state plus logs."""
    logs: list[AgentLogEntry] = []

    input_summary = f"company_name={state.get('company_name', '')}"
    state = run_research_agent(state)
    append_log(
        logs,
        create_log_entry(
            agent_name="research_agent",
            input_summary=input_summary,
            output_summary=(
                f"industry={state.get('industry', '')}, "
                f"company_stage={state.get('company_stage', '')}, "
                f"persona={state.get('persona', '')}, "
                f"pain_points={len(state.get('pain_points', []))}"
            ),
            reasoning="Generated structured company context from the company name.",
        ),
    )

    input_summary = (
        f"persona={state.get('persona', '')}, "
        f"pain_points={len(state.get('pain_points', []))}, "
        f"industry={state.get('industry', '')}"
    )
    state = run_outreach_agent(state)
    append_log(
        logs,
        create_log_entry(
            agent_name="outreach_agent",
            input_summary=input_summary,
            output_summary=(
                f"initial_email_words={_word_count(str(state.get('initial_email', '')))}, "
                f"last_email_words={_word_count(str(state.get('last_email', '')))}"
            ),
            reasoning="Generated personalized outreach email using research context.",
        ),
    )

    input_summary = f"last_email_words={_word_count(str(state.get('last_email', '')))}"
    state = run_monitoring_module(state)
    append_log(
        logs,
        create_log_entry(
            agent_name="monitoring_module",
            input_summary=input_summary,
            output_summary=(
                f"last_contact_days={state.get('last_contact_days', 0)}, "
                f"engagement_status={state.get('engagement_status', '')}"
            ),
            reasoning="Applied deterministic inactivity simulation after outreach.",
        ),
    )

    input_summary = (
        f"last_contact_days={state.get('last_contact_days', 0)}, "
        f"engagement_status={state.get('engagement_status', '')}"
    )
    state = run_risk_detection_agent(state)
    append_log(
        logs,
        create_log_entry(
            agent_name="risk_detection_agent",
            input_summary=input_summary,
            output_summary=(
                f"risk_level={state.get('risk_level', '')}, "
                f"risk_reason={state.get('risk_reason', '')}"
            ),
            reasoning="Classified risk based on inactivity thresholds.",
        ),
    )

    input_summary = (
        f"risk_level={state.get('risk_level', '')}, "
        f"risk_reason={state.get('risk_reason', '')}, "
        f"last_email_words={_word_count(str(state.get('last_email', '')))}"
    )
    state = run_recovery_agent(state)
    append_log(
        logs,
        create_log_entry(
            agent_name="recovery_agent",
            input_summary=input_summary,
            output_summary=(
                f"recovery_strategy={state.get('recovery_strategy', '')}, "
                f"last_email_words={_word_count(str(state.get('last_email', '')))}"
            ),
            reasoning="Generated risk-adaptive recovery strategy and follow-up email.",
        ),
    )

    return {
        "final_state": state,
        "logs": logs,
    }


def _word_count(text: str) -> int:
    return len([token for token in text.split() if token])
