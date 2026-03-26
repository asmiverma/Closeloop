# Closeloop

Closeloop is an autonomous sales recovery system that detects at-risk opportunities, classifies deal risk, and generates targeted recovery actions with full decision traceability.

## What It Delivers

- Multi-agent workflow from company intelligence to recovery messaging
- Deterministic monitoring and risk scoring logic for explainability
- Structured logging for every agent decision
- Professional dark dashboard for fast executive demos
- Demo Mode for quota-safe walkthroughs without external API calls

## Workflow Pipeline

1. Company Intelligence
2. Initial Outreach
3. Engagement Monitoring
4. Risk Analysis
5. Recovery Action

Each execution returns:

- final_state: the fully updated workflow state
- logs: ordered agent trace including input summary, output summary, and reasoning

## Project Structure

### Core

- src/closeloop/state.py: shared workflow state schema and initializer
- src/closeloop/orchestrator.py: sequential execution pipeline
- src/closeloop/logging_layer.py: typed audit log structures

### Agents

- src/closeloop/agents/research_agent.py: company and persona enrichment
- src/closeloop/agents/outreach_agent.py: initial message generation
- src/closeloop/agents/monitoring_module.py: deterministic inactivity simulation
- src/closeloop/agents/risk_detection_agent.py: rule-based risk classification
- src/closeloop/agents/recovery_agent.py: risk-adaptive follow-up generation

### Interface and Tests

- app.py: production-style Streamlit dashboard (Phase 9 UI)
- tests/test_phase1_structure.py: integration-safe mocked orchestrator tests

## Current Implementation Status

- Phase 1: scaffolding and state model complete
- Phase 2: research agent complete
- Phase 3: outreach agent complete
- Phase 4: monitoring module complete
- Phase 5: risk detection complete
- Phase 6: recovery agent complete
- Phase 7: orchestrator and audit logging complete
- Phase 8: end-to-end demo flow complete
- Phase 9: enterprise dashboard redesign complete

## UI Capabilities (Phase 9)

- Dark, high-contrast dashboard with custom CSS design tokens
- Clean card-based information hierarchy
- Risk-emphasized analysis panel
- Code-style email rendering for readability
- Collapsible decision trace with per-agent detail cards
- Highlighted summary banner for final outcome
- Demo Mode toggle for no-quota walkthroughs
- Live Mode for Gemini-backed execution when quota is available

## Setup

### Requirements

- Python 3.13+
- Streamlit
- google-generativeai
- python-dotenv
- pytest

### Environment

Create or update .env in project root:

GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash

GEMINI_MODEL is optional.

## Run the Dashboard

1. Install dependencies in your virtual environment
2. Start Streamlit:

streamlit run app.py

3. Enter a company name and click Run Workflow

If API quota is exceeded, keep Demo Mode enabled for a full product walkthrough.

## Run Tests

pytest -q

The tests are API-independent and should pass without external calls.

## Programmatic Execution

from closeloop.orchestrator import run_sales_workflow
from closeloop.state import create_initial_state

state = create_initial_state("Acme Corp")
result = run_sales_workflow(state)

print(result["final_state"])
print(result["logs"])

## Reliability Notes

- If you see HTTP 429 quota errors, this is a Gemini project-level quota constraint.
- API keys from the same project share quota pools.
- Demo Mode is included to ensure uninterrupted demos.

## Next Roadmap

- Persistence layer for workflow history and analytics
- CRM/webhook integration for production operations
- Outcome feedback loop for strategy optimization
- Comparative campaign benchmarking across segments

## License

Internal project use.
