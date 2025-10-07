# Agent Development Guide

This guide complements the main README and getting-started instructions with the specifics you need when building or extending agents in this repository.

## Prerequisites

- Complete the setup steps in `docs/getting-started.md` (`./scripts/setup.sh` creates `.venv/` and `uv.lock` on first run).
- Activate the environment with `source .venv/bin/activate` or prefix commands with `uv run`.
- Keep dependencies in sync with `uv pip sync uv.lock`; regenerate the lock when upgrading packages using `uv pip compile requirements.txt -o uv.lock`.

## Project Layout Recap

```
agents/
  agent-template/        # Boilerplate for new agents
  example-agent/         # Demonstrates logging, config, and custom tools
  azure-fsi-landingzone/ # Production landing zone agent (mono + squad)
  azure-compliance-checker/ # Compliance validation agent
shared/
  agents.py              # Base classes (BaseClaudeAgent, InteractiveAgent)
  utils/                 # Config, logging, validation helpers
docs/
  getting-started.md     # Setup walkthrough
  agent-guide.md         # <— You are here
```

## Creating a New Agent

1. Copy the template:
   ```bash
   cp -r agents/agent-template agents/my-agent
   cd agents/my-agent
   ```
2. Update `config.yaml` with agent metadata, model, and allowed tools.
3. Implement behaviour in `agent.py`:
   - Inherit from `InteractiveAgent` for REPL-style interaction.
   - Override hooks such as `get_system_prompt()` when you need custom instructions.
   - Register tool functions with the `@tool` decorator from `claude_agent_sdk`.
4. Add optional dependencies in `requirements.txt` if the agent needs extras; run `uv pip install -r requirements.txt` followed by `uv pip compile requirements.txt -o ../../uv.lock` to capture them.
5. Document the new agent with a README inside its directory.

## Working With Tools

- Use the `@tool("name", "Description", {"param": type})` decorator.
- Tool functions must return `{"content": [{"type": "text", "text": "<result>"}]}`.
- Register custom tools by returning them in `get_custom_tools()`.
- See `agents/example-agent/tools/` for small examples and the Azure FSI agent for complex usages.

## Configuration Patterns

- Configuration hierarchy: defaults in code < per-agent `config.yaml` < environment variables (load from `.env`).
- Use `shared.utils.config.load_config()` when you need repository-wide settings.
- Sensitive values (API keys, subscription IDs, etc.) belong in `.env`, never hard-code them.

## Testing

- Run the full suite from the repository root:
  ```bash
  uv run pytest tests/
  ```
- Add new tests in `tests/test_repository.py` or create agent-specific test modules under `tests/`.
- Async tests should use `pytest-asyncio` (`@pytest.mark.asyncio`).
- For quick sanity checks of the shared infrastructure, execute `uv run python scripts/test_setup.py`.

## Logging and Diagnostics

- Import `get_logger` from `shared.utils.logging` to obtain a configured logger.
- Logs are written to `logs/<agent>_<timestamp>.log`; ensure the directory exists via `mkdir -p logs` in setup code.
- For verbose debugging, adjust the log level using `setup_logging("DEBUG")`.

## Coding Standards

- Python ≥ 3.10, type hints encouraged.
- Format with `black`, lint with `flake8`, type-check with `mypy` (run via `uv run <tool>`).
- Keep documentation centralized in `docs/`; update existing files instead of introducing duplicates.
- When adding features, tick or append tasks in `docs/project/roadmap.md` per the repository contribution guidelines.

## Next Steps

- Review `agents/example-agent/README.md` for a guided tour of the example agent.
- Explore the Azure FSI landing zone agent to understand advanced patterns (multi-agent squad, delegation tools, AVM integration).
- Consult `AGENTS.md` whenever you work with automated coding assistants—they read that file for project-specific instructions.
