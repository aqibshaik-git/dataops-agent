"""A fake Anthropic client so tests run with no network and no API key."""
from types import SimpleNamespace


def _message(text, input_tokens, output_tokens, stop_reason):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        usage=SimpleNamespace(input_tokens=input_tokens, output_tokens=output_tokens),
        stop_reason=stop_reason,
    )


class _Stream:
    def __init__(self, chunks, final):
        self.text_stream = iter(chunks)
        self._final = final

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self._final


class FakeClient:
    def __init__(self, chunks=("Hello", " world"), input_tokens=12, output_tokens=4, stop_reason="end_turn"):
        final = _message("".join(chunks), input_tokens, output_tokens, stop_reason)
        self.calls = []
        fake = self

        class _Messages:
            def stream(self, **kwargs):
                fake.calls.append(("stream", kwargs))
                return _Stream(list(chunks), final)

            def create(self, **kwargs):
                fake.calls.append(("create", kwargs))
                return final

        self.messages = _Messages()
