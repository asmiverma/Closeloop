from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from closeloop.logging_layer import WorkflowExecutionResult
from closeloop.orchestrator import run_sales_workflow
from closeloop.state import create_initial_state

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Closeloop", layout="wide")
st.title("🎯 Closeloop Sales Workflow")
st.caption("Multi-agent sales recovery automation system with structured audit logging")

st.divider()

# Demo mode toggle
col_mode = st.columns([4, 1])[1]
with col_mode:
    use_demo = st.toggle("📋 Demo Mode", value=True, help="Use realistic mock data (no API calls)")

st.divider()

col_input, col_button = st.columns([3, 1])
with col_input:
    company_name = st.text_input(
        "Company name",
        placeholder="e.g., Acme Corp, TechStart Inc.",
        label_visibility="collapsed",
    )
with col_button:
    run_clicked = st.button("▶ Run Workflow", use_container_width=True)

st.divider()


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
        st.error("❌ Please enter a company name.")
    else:
        try:
            with st.spinner("🔄 Analyzing and processing workflow..."):
                if use_demo:
                    result = get_demo_result(company_name)
                    st.info("📋 Running in **Demo Mode** with realistic mock data (no API calls)")
                else:
                    state = create_initial_state(company_name)
                    result = run_sales_workflow(state)

            final_state = result["final_state"]
            logs = result["logs"]

            # STEP 1: Research
            st.subheader("📊 Step 1 — Research")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Industry:** `{final_state.get('industry', 'N/A')}`")
                st.markdown(f"**Stage:** `{final_state.get('company_stage', 'N/A')}`")
            with col2:
                st.markdown(f"**Persona:** `{final_state.get('persona', 'N/A')}`")
                pain_points = final_state.get("pain_points", [])
                pain_text = ", ".join(pain_points) if pain_points else "N/A"
                st.markdown(f"**Pain Points:** `{pain_text}`")

            st.divider()

            # STEP 2: Initial Outreach
            st.subheader("✉️ Step 2 — Initial Outreach")
            initial_email = final_state.get("initial_email", "N/A")
            st.markdown(f"> {initial_email}")

            st.divider()

            # STEP 3: Engagement Status
            st.subheader("📅 Step 3 — Engagement Status")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Days Since Contact",
                    final_state.get("last_contact_days", 0),
                    delta=None,
                )
            with col2:
                status_val = final_state.get("engagement_status", "N/A")
                status_color = "🔴" if status_val == "NO_RESPONSE" else "🟢"
                st.markdown(f"**Status:** {status_color} `{status_val}`")

            st.divider()

            # STEP 4: Risk Analysis
            st.subheader("⚠️ Step 4 — Risk Analysis")
            risk_level = final_state.get("risk_level", "N/A")
            risk_colors = {
                "HIGH": "🔴",
                "MEDIUM": "🟡",
                "LOW": "🟢",
            }
            risk_icon = risk_colors.get(risk_level, "⚫")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Risk Level:** {risk_icon} `{risk_level}`")
            with col2:
                st.markdown(
                    f"**Risk Reason:** `{final_state.get('risk_reason', 'N/A')}`"
                )

            st.divider()

            # STEP 5: Recovery Action
            st.subheader("🚀 Step 5 — Recovery Action")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f"**Strategy:** `{final_state.get('recovery_strategy', 'N/A')}`"
                )
            with col2:
                pass
            last_email = final_state.get("last_email", "N/A")
            st.markdown("**Follow-up Email:**")
            st.markdown(f"> {last_email}")

            st.divider()

            # DECISION TRACE: Logs
            st.subheader("🔍 Decision Trace")
            with st.expander("View detailed agent decisions and reasoning", expanded=True):
                for idx, log in enumerate(logs, start=1):
                    st.markdown(f"**Agent {idx}: {log['agent_name'].replace('_', ' ').title()}**")
                    st.markdown(f"*Input:* {log['input_summary']}")
                    st.markdown(f"*Decision:* {log['output_summary']}")
                    st.markdown(f"*Reasoning:* {log['reasoning']}")
                    st.markdown("---")

            st.divider()

            # FINAL SUMMARY
            st.subheader("📋 Final Summary")
            col1, col2 = st.columns(2)
            with col1:
                status_emoji = "🔴" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"
                st.markdown(f"**Deal Status:** {status_emoji} `At Risk - {risk_level}`")
            with col2:
                st.markdown(
                    f"**Action Taken:** `Recovery Triggered - {final_state.get('recovery_strategy', 'N/A')}`"
                )

            st.success("✅ Workflow completed successfully!")

        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ Workflow error: {error_msg[:200]}")
            
            if "quota" in error_msg.lower() or "429" in error_msg:
                st.warning(
                    "⚠️ **API Quota Exceeded** — The free-tier Gemini API has reached its limit.\n\n"
                    "**Solution:** Toggle **📋 Demo Mode** at the top to see the full workflow with realistic mock data (no API calls required)."
                )
            else:
                st.info(
                    "💡 **Tip:** Ensure `GEMINI_API_KEY` is set in `.env` file for live mode, or use Demo Mode above."
                )
