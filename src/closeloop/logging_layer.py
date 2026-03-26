from __future__ import annotations

from typing import TypedDict


class AgentLogEntry(TypedDict):
    agent_name: str
    input_summary: str
    output_summary: str
    reasoning: str


class WorkflowExecutionResult(TypedDict):
    final_state: dict[str, object]
    logs: list[AgentLogEntry]


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


def append_log(logs: list[AgentLogEntry], entry: AgentLogEntry) -> None:
    """Append a log entry while keeping execution order explicit."""
    logs.append(entry)


def render_logs(logs: list[AgentLogEntry]) -> str:
    """Render logs into a human-readable ordered audit string."""
    lines: list[str] = []
    for idx, entry in enumerate(logs, start=1):
        lines.append(
            f"{idx}. {entry['agent_name']} | input: {entry['input_summary']} | "
            f"output: {entry['output_summary']} | reasoning: {entry['reasoning']}"
        )
    return "\n".join(lines)
