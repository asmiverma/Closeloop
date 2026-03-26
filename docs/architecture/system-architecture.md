# System Architecture

Closeloop is a closed-loop sales recovery system that combines LLM-based content generation with deterministic risk logic.

## Architecture Goals

- Keep the workflow understandable from end to end
- Separate deterministic risk logic from LLM generation
- Preserve decision traceability for every workflow run
- Enable demo-safe operation when API quota is limited

## Core Components

1. UI Layer (`app.py`)

- Collects inputs and mode toggles
- Runs workflow and renders output cards
- Displays structured decision logs

2. Orchestration Layer (`src/closeloop/orchestrator.py`)

- Executes the five-step pipeline in strict order
- Passes and returns a shared state object
- Appends structured logs per step

3. State Layer (`src/closeloop/state.py`)

- Defines `SalesWorkflowState`
- Provides `create_initial_state(company_name)`

4. Logging Layer (`src/closeloop/logging_layer.py`)

- Defines typed log entries
- Produces ordered execution trace

5. Agent Layer (`src/closeloop/agents/`)

- `research_agent.py`: enriches company and persona context
- `outreach_agent.py`: writes the initial email
- `monitoring_module.py`: updates inactivity and engagement
- `risk_detection_agent.py`: computes risk level and reason
- `recovery_agent.py`: generates strategy and follow-up

## Data Flow

1. User submits company input from dashboard
2. Orchestrator runs each agent sequentially
3. Each stage updates shared workflow state
4. Logging layer records stage input/output summary
5. UI renders final state and full decision trace

## Diagrams

- Component diagram: `docs/architecture/component-diagram.mmd`
- Sequence diagram: `docs/architecture/workflow-sequence.mmd`

## Design Decisions

- LLM calls are isolated to research, outreach, and recovery
- Risk scoring is deterministic for explainability
- Output is always returned as state + logs
- Demo and cache paths keep UX stable under quota limits
