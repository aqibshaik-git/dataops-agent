"""Load model settings and prices from config.toml (never hard-code prices)."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Pricing:
    """USD per million tokens. Long-context rates apply when input exceeds the threshold."""

    input_per_mtok: float
    output_per_mtok: float
    long_context_threshold: int | None = None
    long_input_per_mtok: float | None = None
    long_output_per_mtok: float | None = None


@dataclass(frozen=True)
class Config:
    model: str
    max_tokens: int
    pricing: Pricing


def load_config(path: str | Path = "config.toml") -> Config:
    data = tomllib.loads(Path(path).read_text())
    model = data["model"]["name"]
    prices = data["pricing"][model]
    return Config(
        model=model,
        max_tokens=int(data["model"].get("max_tokens", 1024)),
        pricing=Pricing(**prices),
    )
