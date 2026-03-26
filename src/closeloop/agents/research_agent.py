from __future__ import annotations

import json
import os
from typing import Any

import google.generativeai as genai

from closeloop.state import SalesWorkflowState


def run_research_agent(state: SalesWorkflowState) -> SalesWorkflowState:
    """Populate structured research context for the provided company name.

    This function performs exactly one Gemini API call and updates state in-place.
    """
    company_name = state.get("company_name", "").strip()
    if not company_name:
        raise ValueError("state['company_name'] is required and must be non-empty.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        "Return ONLY valid JSON with keys: industry, company_stage, persona, pain_points. "
        "company_stage must be one of early-stage, growth-stage, enterprise. "
        "pain_points must be an array of 2 to 3 concise actionable business pain points. "
        "No markdown. No commentary. "
        f"Company name: {company_name}"
    )

    response = model.generate_content(prompt)
    raw_text = getattr(response, "text", "") or ""
    parsed = _parse_research_json(raw_text)
    _validate_research_payload(parsed)

    state["industry"] = parsed["industry"]
    state["company_stage"] = parsed["company_stage"]
    state["persona"] = parsed["persona"]
    state["pain_points"] = parsed["pain_points"]
    return state


def _parse_research_json(raw_text: str) -> dict[str, Any]:
    if not raw_text.strip():
        raise ValueError("Gemini returned empty content for research_agent.")

    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    # Fallback extraction in case model wraps JSON with stray text.
    if not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Gemini output is not valid JSON object text.")
        text = text[start : end + 1]

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to decode research_agent JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("research_agent output must be a JSON object.")
    return payload


def _validate_research_payload(payload: dict[str, Any]) -> None:
    required = ["industry", "company_stage", "persona", "pain_points"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"research_agent output missing required fields: {missing}")

    industry = payload["industry"]
    company_stage = payload["company_stage"]
    persona = payload["persona"]
    pain_points = payload["pain_points"]

    if not isinstance(industry, str) or not industry.strip():
        raise ValueError("'industry' must be a non-empty string.")

    allowed_stages = {"early-stage", "growth-stage", "enterprise"}
    if not isinstance(company_stage, str) or company_stage not in allowed_stages:
        raise ValueError("'company_stage' must be one of early-stage, growth-stage, enterprise.")

    if not isinstance(persona, str) or not persona.strip():
        raise ValueError("'persona' must be a non-empty string.")

    if not isinstance(pain_points, list):
        raise ValueError("'pain_points' must be a list.")
    if len(pain_points) < 2 or len(pain_points) > 3:
        raise ValueError("'pain_points' must contain 2 to 3 items.")

    clean_points: list[str] = []
    for item in pain_points:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("Each pain point must be a non-empty string.")
        clean_points.append(item.strip())

    payload["industry"] = industry.strip()
    payload["persona"] = persona.strip()
    payload["pain_points"] = clean_points
