from __future__ import annotations

from typing import TypedDict


class AgentLogEntry(TypedDict):
    agent_name: str
    input_summary: str
    output_summary: str
    reasoning: str


def create_log_entry(
    agent_name: str,
    input_summary: str,
    output_summary: str,
    reasoning: str,
) -> AgentLogEntry:
    """Create a single structured log entry for later workflow logging."""
    return {
        "agent_name": agent_name,
        "input_summary": input_summary,
        "output_summary": output_summary,
        "reasoning": reasoning,
    }
