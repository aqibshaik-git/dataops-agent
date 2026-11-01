# dataops-agent

A terminal agent with a data engineer's job, running on payments-platform.

## Commands
- Install: `uv sync` · Test: `uv run pytest` · Lint: `uv run ruff check`
- Run: `uv run agent "question"` (flags: `--no-stream`, `--max-tokens N`, `--system FILE`)

## Rules
- The API key lives only in `.env` (git-ignored). Never print, log or commit it.
- Tests never call the real API; use `tests/fakes.py`.
- Aqib writes most of the code. Give hints first; full code only when asked.
