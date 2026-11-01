"""One model call, streamed or not, with timing and usage captured."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable


@dataclass
class CallResult:
    text: str
    input_tokens: int
    output_tokens: int
    stop_reason: str | None
    first_token_ms: float  # time until the first text arrived (whole reply when not streaming)
    total_ms: float


def make_client():
    """Create the real Anthropic client. Reads ANTHROPIC_API_KEY from the environment."""
    import anthropic  # imported lazily so tests never need the SDK or a key

    return anthropic.Anthropic()


def ask(
    client,
    prompt: str,
    *,
    model: str,
    max_tokens: int,
    system: str | None = None,
    stream: bool = True,
    on_text: Callable[[str], None] = lambda s: None,
    clock: Callable[[], float] = time.perf_counter,
) -> CallResult:
    kwargs = dict(model=model, max_tokens=max_tokens,
                  messages=[{"role": "user", "content": prompt}])
    if system:
        kwargs["system"] = system

    start = clock()
    first: float | None = None
    parts: list[str] = []

    if stream:
        with client.messages.stream(**kwargs) as s:
            for chunk in s.text_stream:
                if first is None:
                    first = clock()
                parts.append(chunk)
                on_text(chunk)
            final = s.get_final_message()
    else:
        final = client.messages.create(**kwargs)
        first = clock()
        text = "".join(b.text for b in final.content if getattr(b, "type", None) == "text")
        parts.append(text)
        on_text(text)

    end = clock()
    return CallResult(
        text="".join(parts),
        input_tokens=final.usage.input_tokens,
        output_tokens=final.usage.output_tokens,
        stop_reason=final.stop_reason,
        first_token_ms=((first or end) - start) * 1000,
        total_ms=(end - start) * 1000,
    )
