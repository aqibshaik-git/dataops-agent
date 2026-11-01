from dataops_agent.llm import ask
from tests.fakes import FakeClient


def ticking_clock(step=0.1):
    t = {"now": 0.0}

    def clock():
        t["now"] += step
        return t["now"]

    return clock


def test_stream_collects_text_and_usage():
    seen = []
    r = ask(FakeClient(), "hi", model="m", max_tokens=10, on_text=seen.append, clock=ticking_clock())
    assert seen == ["Hello", " world"]
    assert r.text == "Hello world"
    assert (r.input_tokens, r.output_tokens, r.stop_reason) == (12, 4, "end_turn")
    assert 0 < r.first_token_ms < r.total_ms


def test_no_stream_uses_create():
    client = FakeClient()
    r = ask(client, "hi", model="m", max_tokens=10, stream=False)
    assert client.calls[0][0] == "create"
    assert r.text == "Hello world"


def test_system_prompt_only_sent_when_given():
    client = FakeClient()
    ask(client, "hi", model="m", max_tokens=10)
    ask(client, "hi", model="m", max_tokens=10, system="be brief")
    assert "system" not in client.calls[0][1]
    assert client.calls[1][1]["system"] == "be brief"
