from __future__ import annotations

from typing import TypedDict


class SalesWorkflowState(TypedDict):
    company_name: str
    industry: str
    company_stage: str
    persona: str
    pain_points: list[str]
    initial_email: str
    last_email: str
    last_contact_days: int
    engagement_status: str
    risk_level: str
    risk_reason: str
    recovery_strategy: str


def create_initial_state(company_name: str) -> SalesWorkflowState:
    """Create the shared state object with required keys and neutral defaults."""
    return {
        "company_name": company_name,
        "industry": "",
        "company_stage": "",
        "persona": "",
        "pain_points": [],
        "initial_email": "",
        "last_email": "",
        "last_contact_days": 0,
        "engagement_status": "",
        "risk_level": "",
        "risk_reason": "",
        "recovery_strategy": "",
    }
