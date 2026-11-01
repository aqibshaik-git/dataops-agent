# dataops-agent

A terminal agent with a data engineer's job. It watches the checks on [payments-platform](../payments-platform), investigates incidents (lineage, logs, runbooks via retrieval), reconciles marts against the ledger, and drafts dbt fixes as pull requests, behind an approval gate.

Python core: the agent loop, tools, MCP server, retrieval, evals and tracing. OpenTUI (TypeScript) front end in `tui/` from week 2.

Status: being built through November 2026.

## Run
```
uv sync
cp .env.example .env      # add your ANTHROPIC_API_KEY
uv run pytest
uv run agent "explain Kafka consumer groups in 3 lines"
```
