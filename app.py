from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from closeloop.logging_layer import WorkflowExecutionResult
from closeloop.orchestrator import run_sales_workflow
from closeloop.state import create_initial_state

load_dotenv()

st.set_page_config(page_title="Closeloop", layout="wide")
st.markdown(
    """
<style>
    .stApp {
        background-color: #0B0F14;
        color: #E5E7EB;
    }

    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #E5E7EB;
        margin-bottom: 0.25rem;
    }

    .subtitle {
        color: #9CA3AF;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E5E7EB;
        margin: 0 0 0.75rem 0;
    }

    .card {
        background: #121821;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 18px 20px;
        margin: 0 0 14px 0;
    }

    .muted {
        color: #9CA3AF;
    }

    .risk-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        border: 1px solid transparent;
    }

    .risk-high {
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border-color: rgba(239, 68, 68, 0.45);
    }

    .risk-medium {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border-color: rgba(245, 158, 11, 0.45);
    }

    .risk-low {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border-color: rgba(16, 185, 129, 0.45);
    }

    .summary-banner {
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.22) 0%, rgba(59, 130, 246, 0.08) 100%);
        border: 1px solid rgba(59, 130, 246, 0.5);
        border-radius: 14px;
        padding: 18px 20px;
        margin-top: 8px;
    }

    .summary-k {
        color: #9CA3AF;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .summary-v {
        color: #E5E7EB;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='main-title'>Closeloop</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Autonomous Sales Recovery System</div>",
    unsafe_allow_html=True,
)

toolbar_left, toolbar_right = st.columns([4, 1])
with toolbar_right:
    use_demo = st.toggle("Demo Mode", value=True, help="Run with mock output without API calls")

st.markdown("<div class='section-title'>Input</div>", unsafe_allow_html=True)
input_col, button_col = st.columns([4, 1])
with input_col:
    company_name = st.text_input(
        "Company Name",
        placeholder="Acme Corp",
        label_visibility="collapsed",
    )
with button_col:
    run_clicked = st.button("Run Workflow", use_container_width=True)


def get_demo_result(company_name: str) -> WorkflowExecutionResult:
    """Return realistic mock workflow result for demo purposes."""
    industry_map = {
        "stripe": "Fintech",
        "acme": "Manufacturing",
        "techstart": "SaaS",
        "openai": "AI/ML",
    }
    industry = industry_map.get(company_name.lower().split()[0], "Enterprise Software")

    return {
        "final_state": {
            "company_name": company_name,
            "industry": industry,
            "company_stage": "Series B",
            "persona": "Head of Operations",
            "pain_points": [
                "inefficient sales workflows",
                "lost deals due to poor follow-up",
                "manual email tracking",
            ],
            "initial_email": f"Hi there! We help companies like {company_name} streamline their sales recovery process. Our AI-powered system automatically identifies at-risk deals and triggers targeted recovery campaigns.",
            "last_email": f"Quick follow-up on our conversation about improving {company_name}'s sales recovery rate. We've seen similar companies reduce deal loss by 40% with our system.",
            "last_contact_days": 10,
            "engagement_status": "NO_RESPONSE",
            "risk_level": "HIGH",
            "risk_reason": "No response after 10 days of initial contact",
            "recovery_strategy": "Send urgency-driven follow-up with case study proof",
        },
        "logs": [
            {
                "agent_name": "research_agent",
                "input_summary": f"company_name={company_name}",
                "output_summary": f"industry={industry}, company_stage=Series B, persona=Head of Operations, pain_points=3",
                "reasoning": "Generated structured company context from company name using industry patterns.",
            },
            {
                "agent_name": "outreach_agent",
                "input_summary": "persona=Head of Operations, pain_points=3, industry=Enterprise Software",
                "output_summary": "initial_email_words=42, last_email_words=38",
                "reasoning": "Generated personalized outreach email addressing specific pain points with value proposition.",
            },
            {
                "agent_name": "monitoring_module",
                "input_summary": "last_email_words=38",
                "output_summary": "last_contact_days=10, engagement_status=NO_RESPONSE",
                "reasoning": "Applied deterministic inactivity simulation: 10 days passed without response.",
            },
            {
                "agent_name": "risk_detection_agent",
                "input_summary": "last_contact_days=10, engagement_status=NO_RESPONSE",
                "output_summary": "risk_level=HIGH, risk_reason=No response after 10 days",
                "reasoning": "Classified as HIGH risk: >7 days without engagement indicates cooling deal.",
            },
            {
                "agent_name": "recovery_agent",
                "input_summary": "risk_level=HIGH, risk_reason=No response after 10 days, last_email_words=38",
                "output_summary": "recovery_strategy=Send urgency-driven follow-up with case study proof, last_email_words=42",
                "reasoning": "Generated HIGH-risk recovery strategy: urgent follow-up with social proof to re-engage.",
            },
        ],
    }


if run_clicked:
    if not company_name.strip():
        st.error("Please enter a company name.")
    else:
        try:
            with st.spinner("Running workflow..."):
                if use_demo:
                    result = get_demo_result(company_name)
                    st.info("Running in demo mode with mock data.")
                else:
                    state = create_initial_state(company_name)
                    result = run_sales_workflow(state)

            final_state = result["final_state"]
            logs = result["logs"]

            risk_level = str(final_state.get("risk_level", "UNKNOWN")).upper()
            risk_badge_map = {
                "HIGH": "risk-high",
                "MEDIUM": "risk-medium",
                "LOW": "risk-low",
            }
            risk_badge = risk_badge_map.get(risk_level, "risk-medium")

            st.markdown("<div class='section-title'>Step 1: Company Intelligence</div>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            left, right = st.columns(2)
            with left:
                st.markdown(f"**Industry**  \\n+{final_state.get('industry', 'N/A')}")
                st.markdown(f"**Company Stage**  \\n+{final_state.get('company_stage', 'N/A')}")
            with right:
                st.markdown(f"**Persona**  \\n+{final_state.get('persona', 'N/A')}")
                st.markdown("**Pain Points**")
                pain_points = final_state.get("pain_points", [])
                if isinstance(pain_points, list) and pain_points:
                    for item in pain_points:
                        st.markdown(f"- {item}")
                else:
                    st.markdown("- N/A")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Step 2: Initial Outreach</div>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.code(str(final_state.get("initial_email", "N/A")), language="text")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Step 3: Engagement Status</div>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            left, right = st.columns(2)
            with left:
                st.metric("Days Since Contact", int(final_state.get("last_contact_days", 0)))
            with right:
                st.markdown("**Status**")
                st.markdown(f"<span class='risk-badge {risk_badge}'>{final_state.get('engagement_status', 'N/A')}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Step 4: Risk Analysis</div>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='muted'>RISK LEVEL</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin: 8px 0 12px 0;'><span class='risk-badge {risk_badge}' style='font-size: 1rem; padding: 8px 14px;'>{risk_level}</span></div>", unsafe_allow_html=True)
            st.markdown("**Risk Reason**")
            st.write(str(final_state.get("risk_reason", "N/A")))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Step 5: Recovery Action</div>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"**Recovery Strategy**  \\n+{final_state.get('recovery_strategy', 'N/A')}")
            st.markdown("**Recovery Email**")
            st.code(str(final_state.get("last_email", "N/A")), language="text")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Decision Trace</div>", unsafe_allow_html=True)
            with st.expander("View decision trace", expanded=False):
                for log in logs:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"**Agent**: {str(log.get('agent_name', 'N/A')).replace('_', ' ').title()}")
                    st.markdown(f"**Input Summary**: {log.get('input_summary', '')}")
                    st.markdown(f"**Output Summary**: {log.get('output_summary', '')}")
                    st.markdown(f"**Reasoning**: {log.get('reasoning', '')}")
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Final Summary</div>", unsafe_allow_html=True)
            st.markdown("<div class='summary-banner'>", unsafe_allow_html=True)
            left, right = st.columns(2)
            with left:
                st.markdown("<div class='summary-k'>Deal Status</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='summary-v'>At Risk - {risk_level}</div>", unsafe_allow_html=True)
            with right:
                st.markdown("<div class='summary-k'>Action Taken</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='summary-v'>Recovery Triggered - {final_state.get('recovery_strategy', 'N/A')}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            st.success("Workflow completed successfully.")

        except Exception as e:
            error_msg = str(e)
            st.error(f"Workflow error: {error_msg[:220]}")

            if "quota" in error_msg.lower() or "429" in error_msg:
                st.warning(
                    "API quota exceeded. Enable Demo Mode to continue the walkthrough without external API calls."
                )
            else:
                st.info(
                    "For live mode, verify GEMINI_API_KEY in .env. You can also use Demo Mode."
                )
