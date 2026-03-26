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


def run_outreach_agent(state: SalesWorkflowState) -> SalesWorkflowState:
    """Generate the initial outreach email from researched context with Gemini."""
    persona = state.get("persona", "").strip()
    industry = state.get("industry", "").strip()
    pain_points = state.get("pain_points", [])

    if not persona or not industry or not isinstance(pain_points, list) or not pain_points:
        raise ValueError("Outreach requires persona, industry, and non-empty pain_points.")

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(_resolve_model_name())

    prompt = (
        "Return ONLY valid JSON with keys: initial_email, last_email. "
        "Each value must be a concise, professional outreach email body. "
        "No markdown. No code fences. "
        f"Persona: {persona}. Industry: {industry}. Pain points: {pain_points}."
    )

    response = model.generate_content(prompt)
    raw = getattr(response, "text", "") or ""
    parsed = _parse_json(raw)

    initial_email = str(parsed.get("initial_email", "")).strip()
    last_email = str(parsed.get("last_email", "")).strip()

    if not initial_email:
        raise ValueError("outreach_agent produced empty initial_email.")
    if not last_email:
        last_email = initial_email

    state["initial_email"] = initial_email
    state["last_email"] = last_email
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
        raise ValueError("Gemini returned empty content for outreach_agent.")

    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            text = "\n".join(lines[1:-1]).strip()

    if not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Gemini output is not a JSON object for outreach_agent.")
        text = text[start : end + 1]

    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("outreach_agent output must be a JSON object.")
    return payload
