from __future__ import annotations

import json
import os
from typing import Any

import google.generativeai as genai

from closeloop.state import SalesWorkflowState


DEFAULT_MODEL_CANDIDATES = [
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-flash-latest",
]


def run_recovery_agent(state: SalesWorkflowState) -> SalesWorkflowState:
    """Generate risk-adaptive recovery strategy and follow-up email with Gemini."""
    risk_level = str(state.get("risk_level", "")).strip().upper()
    risk_reason = str(state.get("risk_reason", "")).strip()
    last_email = str(state.get("last_email", "")).strip()
    persona = str(state.get("persona", "")).strip()

    if not risk_level or not risk_reason or not persona:
        raise ValueError("Recovery requires risk_level, risk_reason, and persona.")

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(_resolve_model_name())

    prompt = (
        "Return ONLY valid JSON with keys: recovery_strategy, new_email_body. "
        "new_email_body must be different from the previous email and include a clear CTA. "
        "No markdown. No code fences. "
        f"Risk level: {risk_level}. Risk reason: {risk_reason}. Persona: {persona}. "
        f"Previous email: {last_email}."
    )

    response = model.generate_content(prompt)
    raw = getattr(response, "text", "") or ""
    parsed = _parse_json(raw)

    strategy = str(parsed.get("recovery_strategy", "")).strip()
    new_email = str(parsed.get("new_email_body", "")).strip()

    if not strategy:
        raise ValueError("recovery_agent produced empty recovery_strategy.")
    if not new_email:
        raise ValueError("recovery_agent produced empty new_email_body.")

    state["recovery_strategy"] = strategy
    state["last_email"] = new_email
    return state


def _resolve_model_name() -> str:
    configured = os.getenv("GEMINI_MODEL", "").strip()
    candidates = [configured] if configured else []
    for candidate in DEFAULT_MODEL_CANDIDATES:
        if candidate not in candidates:
            candidates.append(candidate)

    try:
        available = {
            model.name.removeprefix("models/")
            for model in genai.list_models()
            if "generateContent" in getattr(model, "supported_generation_methods", [])
        }
    except Exception:
        return candidates[0]

    for candidate in candidates:
        if candidate in available:
            return candidate
    return candidates[0]


def _parse_json(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    if not text:
        raise ValueError("Gemini returned empty content for recovery_agent.")

    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()

    if not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Gemini output is not a JSON object for recovery_agent.")
        text = text[start : end + 1]

    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("recovery_agent output must be a JSON object.")
    return payload
