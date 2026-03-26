# Closeloop

A multi-agent sales workflow system for close-loop recovery automation with structured audit logging and a clean Streamlit demo interface.

## Project Structure

### Core

- `src/closeloop/state.py`: shared SalesWorkflowState schema and initializer.
- `src/closeloop/orchestrator.py`: sequential workflow pipeline with per-agent logging.
- `src/closeloop/logging_layer.py`: structured audit log types (AgentLogEntry, WorkflowExecutionResult).

### Agents (Phases 2–6)

- `src/closeloop/agents/research_agent.py`: Gemini-powered research (company context, persona, pain points).
- `src/closeloop/agents/outreach_agent.py`: Gemini-powered cold outreach email generation with 2-attempt retry.
- `src/closeloop/agents/monitoring_module.py`: deterministic inactivity detection (10-day threshold).
- `src/closeloop/agents/risk_detection_agent.py`: rule-based risk classification (HIGH/MEDIUM/LOW).
- `src/closeloop/agents/recovery_agent.py`: Gemini-powered risk-adaptive recovery email strategies.

### Application & Tests

- `app.py`: Phase 8 Streamlit demo with full workflow visualization and decision trace.
- `tests/test_phase1_structure.py`: structure validation with mocked agents (no API required).

## Current Status

✅ **Phase 1**: Project scaffold, state schema, logging infrastructure.  
✅ **Phase 2**: Research agent (Gemini with model fallback).  
✅ **Phase 3**: Outreach agent (Gemini with 2-attempt retry and word-count normalization).  
✅ **Phase 4**: Monitoring module (deterministic 10-day inactivity simulation).  
✅ **Phase 5**: Risk detection agent (rule-based classification).  
✅ **Phase 6**: Recovery agent (Gemini with strict validation and email differentiation).  
✅ **Phase 7**: Logging layer and orchestrator pipeline (sequential execution with per-agent audit trails).  
✅ **Phase 8**: Streamlit demo layer with clear workflow visualization (judges version).

## Architecture Overview

```
Workflow Pipeline:
  Input: company_name → State
  ├─ research_agent (Gemini)
  │  └─ Output: industry, company_stage, persona, pain_points
  ├─ outreach_agent (Gemini)
  │  └─ Output: initial_email, last_email
  ├─ monitoring_module (Deterministic)
  │  └─ Output: last_contact_days, engagement_status
  ├─ risk_detection_agent (Rule-based)
  │  └─ Output: risk_level, risk_reason
  └─ recovery_agent (Gemini)
     └─ Output: recovery_strategy, new_email_body

Logging: Each agent creates one structured log entry (agent_name, input_summary, output_summary, reasoning).
Result: WorkflowExecutionResult = {final_state, logs[]}
UI: Streamlit demo displays all 5 steps + decision trace + final summary.
```

## Environment Setup

### Requirements

- Python 3.13+
- `google-generativeai` SDK
- `pytest` for testing
- Streamlit for demo UI

### Configuration

```bash
# Set Gemini API key
export GEMINI_API_KEY=your_api_key_here

# Optional: override model selection
export GEMINI_MODEL=gemini-2.5-flash
```

## Running Tests

```bash
# Run all tests (mocked agents, no API calls required)
pytest -q

# Run with coverage
pytest --cov=src/closeloop

# Run specific test
pytest tests/test_phase1_structure.py::test_orchestrator_executes_sequential_pipeline -v
```

## Running the Demo UI

```bash
# Start the Streamlit app
streamlit run app.py

# Then enter a company name (e.g., "Acme Corp", "TechStart Inc.") and click "Run Workflow"
# The app displays:
# - Step 1: Research findings (industry, stage, persona, pain points)
# - Step 2: Initial outreach email
# - Step 3: Engagement status metrics
# - Step 4: Risk analysis (level + reason)
# - Step 5: Recovery action (strategy + follow-up email)
# - Decision Trace: Full audit log of agent decisions
# - Final Summary: Deal status and action taken
```

## Running the Full Workflow Programmatically

```python
from closeloop.orchestrator import run_sales_workflow
from closeloop.state import create_initial_state

state = create_initial_state("Your Company Name")
result = run_sales_workflow(state)

print("Final State:", result["final_state"])
print("Audit Logs:\n", result["logs"])
```

## Key Features

- **Gemini Integration**: Auto-fallback across multiple Gemini model candidates for cross-account portability.
- **Deterministic Fallback**: Word-count normalization with CTA preservation on retry failures.
- **Structured Validation**: Input pre-checks, robust JSON extraction, output post-validation.
- **Audit Transparency**: Per-agent logging with input/output summaries and reasoning.
- **Clean State Management**: TypedDict-based immutable-style workflow state.
- **Clean Demo UI**: 5-step workflow visualization with emoji indicators, metrics, and decision trace.

## Demo Quick Start

1. **Set API Key** (if running with real Gemini):

   ```bash
   export GEMINI_API_KEY=sk-...
   ```

2. **Start Streamlit App**:

   ```bash
   streamlit run app.py
   ```

3. **Enter Company Name** (e.g., "Stripe", "OpenAI", "Acme Corp"):

   ```
   Enter → Click "Run Workflow"
   ```

4. **View Results**:
   - 📊 Research findings
   - ✉️ Outreach email
   - 📅 Engagement metrics
   - ⚠️ Risk classification
   - 🚀 Recovery strategy
   - 🔍 Full decision trace with agent reasoning

## Test Results

```
$ pytest tests/test_phase1_structure.py -v

tests/test_phase1_structure.py::test_state_initialization_has_required_keys PASSED
tests/test_phase1_structure.py::test_orchestrator_executes_sequential_pipeline PASSED

2 passed in 0.73s
```

All tests pass without requiring external API calls (agents are mocked).

## Next Steps

- Real-time company research integration with external data sources
- A/B test variant generation and tracking
- Outcome measurement and closed-loop feedback
- Database persistence for audit logs and workflow history
- Email delivery and click-through tracking
- Multi-threaded campaign management UI

## License

Internal use only - Closeloop Sales Workflow System
