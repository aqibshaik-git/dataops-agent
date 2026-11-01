"""`agent "your prompt"`: stream one answer, then report tokens, cost and latency."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from .config import load_config
from .cost import call_cost
from .llm import ask, make_client


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agent", description="Ask the model one question.")
    p.add_argument("prompt", help="what to ask")
    p.add_argument("--no-stream", action="store_true", help="wait for the whole reply")
    p.add_argument("--max-tokens", type=int, help="cap on output tokens (overrides config)")
    p.add_argument("--system", type=Path, help="file whose contents become the system prompt")
    p.add_argument("--config", type=Path, default=Path("config.toml"))
    return p


def format_report(result, cost: float, model: str) -> str:
    return (
        f"\n\n--- {model} ---\n"
        f"input tokens : {result.input_tokens}\n"
        f"output tokens: {result.output_tokens}\n"
        f"stop reason  : {result.stop_reason}\n"
        f"cost         : ${cost:.6f}\n"
        f"first token  : {result.first_token_ms:.0f} ms\n"
        f"total        : {result.total_ms:.0f} ms"
    )


def main(argv: list[str] | None = None, client=None) -> int:
    args = build_parser().parse_args(argv)
    load_dotenv()
    cfg = load_config(args.config)
    system = args.system.read_text() if args.system else None

    result = ask(
        client or make_client(),
        args.prompt,
        model=cfg.model,
        max_tokens=args.max_tokens or cfg.max_tokens,
        system=system,
        stream=not args.no_stream,
        on_text=lambda s: print(s, end="", flush=True),
    )
    cost = call_cost(result.input_tokens, result.output_tokens, cfg.pricing)
    print(format_report(result, cost, cfg.model))
    if result.stop_reason == "max_tokens":
        print("note: reply was cut off by max_tokens", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
