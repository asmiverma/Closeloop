# Closeloop

Phase 1 scaffold for a deterministic multi-agent sales workflow.

## Project Structure

- `src/closeloop/state.py`: shared state schema and initializer.
- `src/closeloop/agents/`: agent function signatures (stubs only).
- `src/closeloop/logging_layer.py`: structured log entry schema.
- `src/closeloop/orchestrator.py`: orchestrator function signature (stub only).
- `app.py`: minimal Streamlit placeholder.
- `tests/test_phase1_structure.py`: structure validation tests.

## Current Status

Implemented: Phase 1 only.

Not implemented yet:

- Gemini-backed research, outreach, and recovery logic.
- Monitoring module logic.
- Risk detection logic.
- Sequential orchestration.
- Full Streamlit workflow UI.
- End-to-end tests.
