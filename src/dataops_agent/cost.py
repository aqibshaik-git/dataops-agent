"""Pure cost maths: no API calls, so it is easy to test."""
from __future__ import annotations

from .config import Pricing

MILLION = 1_000_000


def call_cost(input_tokens: int, output_tokens: int, pricing: Pricing) -> float:
    """Cost in USD of one call.

    If the prompt is longer than the long-context threshold, the long-context
    rates apply to the whole call (input and output).
    """
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts cannot be negative")

    in_rate, out_rate = pricing.input_per_mtok, pricing.output_per_mtok
    threshold = pricing.long_context_threshold
    if threshold is not None and input_tokens > threshold:
        in_rate = pricing.long_input_per_mtok or in_rate
        out_rate = pricing.long_output_per_mtok or out_rate

    return input_tokens * in_rate / MILLION + output_tokens * out_rate / MILLION
