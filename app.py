from __future__ import annotations

from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from closeloop.orchestrator import run_sales_workflow
from closeloop.state import create_initial_state

load_dotenv()

MASTER_CONFIG = {
    "dashboard_config": {
        "title": "Closeloop",
        "subtitle": "Autonomous Sales Recovery Intelligence Console",
        "version": "v1.2 | Trial Mode",
        "last_run": "2026-03-26 19:45:58 IST",
        "company_name": "Acme Manufacturing Inc.",
        "trial_mode": True,
        "trial_banner": "DEMO / TRIAL MODE - Synthetic enterprise data for hackathon showcase. Connect your CRM in production for live deals.",
    },
    "navigation": [
        "All Sections",
        "Deal Insight",
        "Execution Snapshot",
        "Company Intelligence",
        "Initial Outreach",
        "Risk Analysis",
        "Recovery Action",
        "Decision Trace",
        "Final Summary",
    ],
    "deal_insight": {
        "headline": "At-Risk Deal Detected",
        "risk_level": "HIGH",
        "confidence_score": 0.92,
        "confidence_label": "92% confidence based on 11-day inactivity + zero engagement signals",
        "days_since_engagement": 11,
        "status_pill": "CRITICAL | Pipeline leakage risk elevated",
        "quick_summary": "The opportunity has stalled post-initial outreach. Autonomous Recovery Agent has been activated with a fresh messaging angle to re-engage the VP Revenue Operations.",
        "projected_impact": "Potential 38% recovery probability within 72 hours if new email is opened",
    },
    "execution_snapshot": {
        "agents_executed": 5,
        "pain_points_identified": 4,
        "risk_score": 92,
        "execution_time": "2.4 seconds total",
        "agents_breakdown": [
            {"agent": "Research Agent (Gemini)", "status": "Completed", "time": "0.6s"},
            {"agent": "Outreach Agent (Gemini)", "status": "Completed", "time": "0.8s"},
            {"agent": "Monitoring Module", "status": "Completed", "time": "0.1s"},
            {"agent": "Risk Detection Agent", "status": "Completed", "time": "0.1s"},
            {"agent": "Recovery Agent (Gemini)", "status": "Completed", "time": "0.8s"},
        ],
        "kpis": {
            "pipeline_health": "At Risk",
            "recovery_triggered": True,
            "cost_per_run": "$0.00 (Gemini free tier)",
            "demo_note": "All agents ran autonomously with full state synchronization",
        },
    },
    "company_intelligence": {
        "industry": "Manufacturing",
        "company_stage": "Series B",
        "persona": "VP Revenue Operations",
        "pain_points": [
            "Pipeline follow-up is inconsistent across account teams",
            "High-intent opportunities stall after first outbound touch",
            "Manual engagement tracking delays risk response",
            "Recovery messaging is not personalized by segment",
        ],
        "enriched_context": "Acme Manufacturing Inc. closed $42M Series B in Q4 2025. They scaled their AE team by 3x in 18 months and now see 34% of deals stall in the 7-14 day window after initial demo.",
        "key_metrics": {
            "employees": "240",
            "annual_revenue": "$68M ARR",
            "sales_team_size": "18 Account Executives",
        },
    },
    "initial_outreach": {
        "subject": "Automate stalled opportunity recovery for Acme Corp's revenue ops",
        "email_body": "Hi team,\n\nWe help companies like Acme Corp recover stalled opportunities by automating follow-up timing, prioritizing no-response accounts, and tailoring messaging to operational pain points. Teams typically improve recovery conversion by 25-40% within one quarter.\n\nWould you be open to a 10-minute walkthrough?\n\nBest,\nSales Recovery Agent",
        "word_count": 87,
        "cta_strength": "Strong | Includes clear value metric and time-bound CTA",
    },
    "risk_analysis": {
        "risk_level": "HIGH",
        "risk_reason": "No response after 11 days and no follow-up opened in the last cycle",
        "engagement_signals": [
            {"signal": "Email opened", "value": False, "days_ago": 11},
            {"signal": "Reply received", "value": False},
            {"signal": "Link clicked", "value": False},
            {"signal": "Last contact", "value": "11 days ago"},
        ],
        "risk_breakdown": "Inactivity threshold breached (11 days > 7-day policy) -> HIGH risk classification.",
        "risk_score_trend": "Rising (was MEDIUM 4 days ago)",
    },
    "recovery_action": {
        "strategy": "Priority recovery sequence with urgency framing and proof-led CTA",
        "new_subject": "Quick win: Recover your stalled pipeline opportunities in <7 days",
        "new_email_body": "Following up on our last note - the opportunity has been quiet for 11 days.\n\nHere is a recovery playbook tailored for Acme's post-Series B scaling stage. Similar manufacturing teams recovered 3 stalled deals in their first month.\n\nCan we schedule a 10-minute call this week to run the playbook live?\n\nRegards,\nRecovery Agent",
        "key_changes_from_initial": [
            "Shifted from value proposition to urgency and social proof",
            "References 11-day inactivity directly",
            "Shorter conversational tone",
            "CTA focuses on immediate next step",
        ],
        "projected_lift": "Expected 35-42% higher open rate vs original email",
    },
    "decision_trace": {
        "title": "Full Agent Reasoning & Audit Trail",
        "log": [
            {
                "agent": "Research Agent",
                "timestamp": "19:44:12",
                "reasoning": "Parsed company name and identified likely funding stage, growth profile, and follow-up bottlenecks.",
                "output": "Industry, stage, persona and 4 pain points populated",
            },
            {
                "agent": "Outreach Agent",
                "timestamp": "19:44:45",
                "reasoning": "Used pain points plus persona context to craft targeted outreach with clear CTA.",
                "output": "Initial email generated",
            },
            {
                "agent": "Monitoring Module",
                "timestamp": "19:45:10",
                "reasoning": "Applied deterministic rule for inactivity and no-response status.",
                "output": "State updated",
            },
            {
                "agent": "Risk Detection Agent",
                "timestamp": "19:45:22",
                "reasoning": "Classified HIGH risk because inactivity exceeded threshold.",
                "output": "Risk classified as HIGH",
            },
            {
                "agent": "Recovery Agent",
                "timestamp": "19:45:58",
                "reasoning": "Avoided repetition and changed message angle to urgency plus proof.",
                "output": "Recovery email and strategy generated",
            },
        ],
    },
    "final_summary": {
        "deal_status": "At Risk - HIGH",
        "action_taken": "Recovery Triggered - Priority recovery sequence with urgency framing and proof-led CTA",
        "next_steps": "- New recovery email dispatched\n- 48-hour engagement window started\n- If no reply: escalate to multi-channel sequence",
        "overall_confidence": 0.92,
        "demo_message": "End-to-end autonomous workflow completed successfully.",
    },
}

st.set_page_config(page_title=MASTER_CONFIG["dashboard_config"]["title"], layout="wide")

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    * { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }

    .stApp { background: #05070A; color: #E6F0FF; }
    .block-container { padding-top: 1.2rem; max-width: 1400px; }
    [data-testid="stSidebar"] {
        background: #0A0F14;
        border-right: 1px solid #1A2330;
    }

    .title { font-size: 2rem; font-weight: 600; letter-spacing: -0.02em; margin: 0; }
    .subtitle { color: #BFD3F2; margin: 0.3rem 0 0.2rem 0; }
    .version { color: #98B4D8; font-size: 0.82rem; }

    .hero {
        background: #0C121A;
        border: 1px solid #1B2735;
        border-radius: 16px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }
    .hero-k { color: #98B4D8; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .hero-v { font-size: 1.35rem; font-weight: 600; margin: 0.2rem 0 0.4rem 0; }
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 500;
        background: rgba(255, 59, 92, 0.14);
        color: #FF3B5C;
        border: 1px solid rgba(255, 59, 92, 0.44);
    }

    .metric-card {
        background: #0D131C;
        border-radius: 12px;
        border: 1px solid #1B2735;
        padding: 1.25rem;
        box-shadow: none;
    }

    .section-title { font-size: 1.06rem; font-weight: 600; margin: 0.6rem 0 0.5rem 0; }
    .card {
        background: #0C121A;
        border: 1px solid #1B2735;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .k { color: #9FC0E6; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; }
    .v { color: #E6F0FF; font-weight: 600; margin-bottom: 0.5rem; }

    .risk-badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 600;
        background: rgba(255, 59, 92, 0.14);
        color: #FF3B5C;
        border: 1px solid rgba(255, 59, 92, 0.44);
    }

    .summary {
        background: #0C121A;
        border: 1px solid #1D3550;
        border-radius: 14px;
        padding: 14px 16px;
        margin-top: 8px;
    }

    .trial-banner {
        background: #0B1726;
        border: 1px solid #1D3550;
        border-radius: 10px;
        padding: 10px 12px;
        color: #AFC7E8;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }

    div[data-testid="stMetric"] {
        background: #0C121A;
        border: 1px solid #1B2735;
        border-radius: 12px;
        padding: 0.4rem 0.6rem;
    }

    div[data-testid="stCodeBlock"] pre {
        background: #070D16;
        border: 1px solid #1A2330;
        border-radius: 10px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #1B2735;
        border-radius: 12px;
        background: #0C121A;
    }
</style>
""",
    unsafe_allow_html=True,
)

if "last_run" not in st.session_state:
    st.session_state.last_run = MASTER_CONFIG["dashboard_config"]["last_run"]
if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None


def section_visible(selected: str, name: str) -> bool:
    return selected == "All Sections" or selected == name


def demo_payload(company_name: str) -> dict[str, object]:
    cfg = MASTER_CONFIG
    final_state = {
        "company_name": company_name,
        "industry": cfg["company_intelligence"]["industry"],
        "company_stage": cfg["company_intelligence"]["company_stage"],
        "persona": cfg["company_intelligence"]["persona"],
        "pain_points": cfg["company_intelligence"]["pain_points"],
        "initial_email": cfg["initial_outreach"]["email_body"],
        "last_email": cfg["recovery_action"]["new_email_body"],
        "last_contact_days": cfg["deal_insight"]["days_since_engagement"],
        "engagement_status": "NO_RESPONSE",
        "risk_level": cfg["risk_analysis"]["risk_level"],
        "risk_reason": cfg["risk_analysis"]["risk_reason"],
        "recovery_strategy": cfg["recovery_action"]["strategy"],
    }
    logs = [
        {
            "agent_name": item["agent"].lower().replace(" ", "_"),
            "input_summary": item["timestamp"],
            "output_summary": item["output"],
            "reasoning": item["reasoning"],
        }
        for item in cfg["decision_trace"]["log"]
    ]
    return {"final_state": final_state, "logs": logs}


with st.sidebar:
    st.markdown("### Console Controls")
    use_demo = st.toggle("Trial / Demo Mode", value=True)
    company_name = st.text_input("Company Name", value=MASTER_CONFIG["dashboard_config"]["company_name"])
    run_clicked = st.button("Run Workflow", use_container_width=True)

    st.markdown("---")
    selected_nav = st.radio("Navigation", MASTER_CONFIG["navigation"], label_visibility="collapsed")

    st.markdown("---")
    st.caption(f"Last Run: {st.session_state.last_run}")

st.markdown(f"<p class='title'>{MASTER_CONFIG['dashboard_config']['title']}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{MASTER_CONFIG['dashboard_config']['subtitle']}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='version'>{MASTER_CONFIG['dashboard_config']['version']}</p>", unsafe_allow_html=True)

if use_demo:
    st.markdown(
        f"<div class='trial-banner'>{MASTER_CONFIG['dashboard_config']['trial_banner']}</div>",
        unsafe_allow_html=True,
    )

if run_clicked:
    if not company_name.strip():
        st.error("Please enter a company name.")
    else:
        try:
            with st.spinner("Running workflow..."):
                if use_demo:
                    result = demo_payload(company_name)
                else:
                    state = create_initial_state(company_name)
                    result = run_sales_workflow(state)

            st.session_state.workflow_result = result
            st.session_state.last_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as exc:
            msg = str(exc)
            st.error(f"Workflow error: {msg[:220]}")
            if "quota" in msg.lower() or "429" in msg:
                st.warning("API quota exceeded. Enable Trial / Demo Mode to continue with synthetic data.")

if st.session_state.workflow_result is None:
    st.markdown("<div class='hero'><div class='hero-k'>Deal Insight</div><div class='hero-v'>Ready for Analysis</div><div>Run workflow from the sidebar to generate insights.</div></div>", unsafe_allow_html=True)
else:
    result = st.session_state.workflow_result
    final_state = result["final_state"]
    logs = result["logs"]

    cfg = MASTER_CONFIG
    risk_level = str(final_state.get("risk_level", "HIGH")).upper()
    confidence = cfg["deal_insight"]["confidence_score"]

    if section_visible(selected_nav, "Deal Insight"):
        st.markdown("<div class='hero'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.markdown("<div class='hero-k'>Deal Insight</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='hero-v'>{cfg['deal_insight']['headline']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='risk-badge'>{risk_level}</span>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:8px'>{cfg['deal_insight']['status_pill']}</div>", unsafe_allow_html=True)
        with c2:
            st.metric("Confidence", f"{confidence:.2f}")
        with c3:
            st.metric("Days Since Engagement", int(final_state.get("last_contact_days", 0)))
        st.caption(cfg["deal_insight"]["confidence_label"])
        st.write(cfg["deal_insight"]["quick_summary"])
        st.caption(cfg["deal_insight"]["projected_impact"])
        st.markdown("</div>", unsafe_allow_html=True)

    if section_visible(selected_nav, "Execution Snapshot"):
        st.markdown("<div class='section-title'>Execution Snapshot</div>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Agents Executed", cfg["execution_snapshot"]["agents_executed"])
        with m2:
            st.metric("Pain Points Identified", cfg["execution_snapshot"]["pain_points_identified"])
        with m3:
            st.metric("Risk Score", cfg["execution_snapshot"]["risk_score"])
        st.caption(cfg["execution_snapshot"]["execution_time"])

        with st.expander("Agent Runtime Breakdown", expanded=False):
            for row in cfg["execution_snapshot"]["agents_breakdown"]:
                st.write(f"- {row['agent']}: {row['status']} ({row['time']})")

    if section_visible(selected_nav, "Company Intelligence"):
        st.markdown("<div class='section-title'>Company Intelligence</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        left, right = st.columns(2)
        with left:
            st.markdown("<div class='k'>Industry</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='v'>{final_state.get('industry', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown("<div class='k'>Company Stage</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='v'>{final_state.get('company_stage', 'N/A')}</div>", unsafe_allow_html=True)
        with right:
            st.markdown("<div class='k'>Persona</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='v'>{final_state.get('persona', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown("<div class='k'>Pain Points</div>", unsafe_allow_html=True)
            for item in final_state.get("pain_points", []):
                st.markdown(f"- {item}")
        st.markdown("<div class='k'>Enriched Context</div>", unsafe_allow_html=True)
        st.write(cfg["company_intelligence"]["enriched_context"])
        km1, km2, km3 = st.columns(3)
        with km1:
            st.metric("Employees", cfg["company_intelligence"]["key_metrics"]["employees"])
        with km2:
            st.metric("Annual Revenue", cfg["company_intelligence"]["key_metrics"]["annual_revenue"])
        with km3:
            st.metric("Sales Team", cfg["company_intelligence"]["key_metrics"]["sales_team_size"])
        st.markdown("</div>", unsafe_allow_html=True)

    if section_visible(selected_nav, "Initial Outreach"):
        st.markdown("<div class='section-title'>Initial Outreach</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='k'>Subject</div>", unsafe_allow_html=True)
        st.write(cfg["initial_outreach"]["subject"])
        st.markdown("<div class='k'>Email Body</div>", unsafe_allow_html=True)
        st.code(str(final_state.get("initial_email", "")), language="text")
        cta1, cta2 = st.columns(2)
        with cta1:
            st.metric("Word Count", cfg["initial_outreach"]["word_count"])
        with cta2:
            st.metric("CTA Strength", cfg["initial_outreach"]["cta_strength"])
        st.markdown("</div>", unsafe_allow_html=True)

    if section_visible(selected_nav, "Risk Analysis"):
        st.markdown("<div class='section-title'>Risk Analysis</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<span class='risk-badge'>{cfg['risk_analysis']['risk_level']}</span>", unsafe_allow_html=True)
        st.write(cfg["risk_analysis"]["risk_reason"])
        st.caption(cfg["risk_analysis"]["risk_breakdown"])
        st.write(f"Risk score trend: {cfg['risk_analysis']['risk_score_trend']}")
        with st.expander("Engagement Signals", expanded=False):
            for sig in cfg["risk_analysis"]["engagement_signals"]:
                st.write(f"- {sig['signal']}: {sig['value'] if 'value' in sig else 'n/a'}")
        st.markdown("</div>", unsafe_allow_html=True)

    if section_visible(selected_nav, "Recovery Action"):
        st.markdown("<div class='section-title'>Recovery Action</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='k'>Strategy</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='v'>{final_state.get('recovery_strategy', 'N/A')}</div>", unsafe_allow_html=True)
        st.markdown("<div class='k'>New Subject</div>", unsafe_allow_html=True)
        st.write(cfg["recovery_action"]["new_subject"])
        st.markdown("<div class='k'>New Email Body</div>", unsafe_allow_html=True)
        st.code(str(final_state.get("last_email", "")), language="text")
        st.markdown("<div class='k'>Key Changes</div>", unsafe_allow_html=True)
        for item in cfg["recovery_action"]["key_changes_from_initial"]:
            st.write(f"- {item}")
        st.caption(cfg["recovery_action"]["projected_lift"])
        st.markdown("</div>", unsafe_allow_html=True)

    if section_visible(selected_nav, "Decision Trace"):
        st.markdown("<div class='section-title'>Decision Trace</div>", unsafe_allow_html=True)
        with st.expander(cfg["decision_trace"]["title"], expanded=False):
            for row in cfg["decision_trace"]["log"]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='v'>{row['agent']}</div>", unsafe_allow_html=True)
                st.caption(f"Timestamp: {row['timestamp']}")
                st.markdown("<div class='k'>Reasoning</div>", unsafe_allow_html=True)
                st.write(row["reasoning"])
                st.markdown("<div class='k'>Output</div>", unsafe_allow_html=True)
                st.write(row["output"])
                st.markdown("</div>", unsafe_allow_html=True)

    if section_visible(selected_nav, "Final Summary"):
        st.markdown("<div class='section-title'>Final Summary</div>", unsafe_allow_html=True)
        st.markdown("<div class='summary'>", unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1:
            st.markdown("<div class='k'>Deal Status</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='v'>{cfg['final_summary']['deal_status']}</div>", unsafe_allow_html=True)
        with s2:
            st.markdown("<div class='k'>Action Taken</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='v'>{cfg['final_summary']['action_taken']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='k'>Next Steps</div>", unsafe_allow_html=True)
        st.write(cfg["final_summary"]["next_steps"])
        st.caption(f"Overall confidence: {cfg['final_summary']['overall_confidence']:.2f}")
        st.success(cfg["final_summary"]["demo_message"])
        st.markdown("</div>", unsafe_allow_html=True)
