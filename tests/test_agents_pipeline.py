from __future__ import annotations

from types import SimpleNamespace

from closeloop.agents.monitoring_module import run_monitoring_module
from closeloop.agents.outreach_agent import run_outreach_agent
from closeloop.agents.recovery_agent import run_recovery_agent
from closeloop.agents.risk_detection_agent import run_risk_detection_agent
from closeloop.orchestrator import run_sales_workflow
from closeloop.state import create_initial_state


def test_monitoring_module_sets_inactivity_defaults() -> None:
    state = create_initial_state("Acme")
    updated = run_monitoring_module(state)

    assert updated["last_contact_days"] == 10
    assert updated["engagement_status"] == "NO_RESPONSE"


def test_risk_detection_high_for_no_response_over_7_days() -> None:
    state = create_initial_state("Acme")
    state["last_contact_days"] = 10
    state["engagement_status"] = "NO_RESPONSE"

    updated = run_risk_detection_agent(state)

    assert updated["risk_level"] == "HIGH"
    assert "10" in updated["risk_reason"]


def test_outreach_agent_parses_gemini_json(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    state = create_initial_state("Acme")
    state["industry"] = "Manufacturing"
    state["persona"] = "VP Revenue Operations"
    state["pain_points"] = ["stalled deals", "manual follow-up"]

    response_text = (
        '{"initial_email":"Hello from outreach","last_email":"Hello from outreach"}'
    )

    class DummyModel:
        def generate_content(self, _prompt: str) -> SimpleNamespace:
            return SimpleNamespace(text=response_text)

    monkeypatch.setattr("closeloop.agents.outreach_agent._resolve_model_name", lambda: "gemini-1.5-flash")
    monkeypatch.setattr("closeloop.agents.outreach_agent.genai.configure", lambda **_kwargs: None)
    monkeypatch.setattr("closeloop.agents.outreach_agent.genai.GenerativeModel", lambda _name: DummyModel())

    updated = run_outreach_agent(state)

    assert updated["initial_email"] == "Hello from outreach"
    assert updated["last_email"] == "Hello from outreach"


def test_recovery_agent_parses_gemini_json(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    state = create_initial_state("Acme")
    state["persona"] = "VP Revenue Operations"
    state["risk_level"] = "HIGH"
    state["risk_reason"] = "No response after 10 days"
    state["last_email"] = "Previous email"

    response_text = (
        '{"recovery_strategy":"Urgency plus proof","new_email_body":"Follow-up with CTA"}'
    )

    class DummyModel:
        def generate_content(self, _prompt: str) -> SimpleNamespace:
            return SimpleNamespace(text=response_text)

    monkeypatch.setattr("closeloop.agents.recovery_agent._resolve_model_name", lambda: "gemini-1.5-flash")
    monkeypatch.setattr("closeloop.agents.recovery_agent.genai.configure", lambda **_kwargs: None)
    monkeypatch.setattr("closeloop.agents.recovery_agent.genai.GenerativeModel", lambda _name: DummyModel())

    updated = run_recovery_agent(state)

    assert updated["recovery_strategy"] == "Urgency plus proof"
    assert updated["last_email"] == "Follow-up with CTA"


def test_orchestrator_runs_with_real_monitoring_and_risk(monkeypatch) -> None:
    state = create_initial_state("Acme")

    def fake_research(s):
        s["industry"] = "Manufacturing"
        s["company_stage"] = "growth-stage"
        s["persona"] = "VP Revenue Operations"
        s["pain_points"] = ["stalled deals", "slow follow-up"]
        return s

    def fake_outreach(s):
        s["initial_email"] = "Initial"
        s["last_email"] = "Initial"
        return s

    def fake_recovery(s):
        s["recovery_strategy"] = "Escalate follow-up"
        s["last_email"] = "Recovery message"
        return s

    monkeypatch.setattr("closeloop.orchestrator.run_research_agent", fake_research)
    monkeypatch.setattr("closeloop.orchestrator.run_outreach_agent", fake_outreach)
    monkeypatch.setattr("closeloop.orchestrator.run_recovery_agent", fake_recovery)

    result = run_sales_workflow(state)

    assert result["final_state"]["engagement_status"] == "NO_RESPONSE"
    assert result["final_state"]["risk_level"] == "HIGH"
    assert len(result["logs"]) == 5
