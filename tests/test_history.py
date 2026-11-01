from dataops_agent.history import trim_history


def count(m):
    return len(m["content"].split())


MSGS = [
    {"role": "user", "content": "one two three"},
    {"role": "assistant", "content": "four five"},
    {"role": "user", "content": "six"},
    {"role": "assistant", "content": "seven eight nine ten"},
    {"role": "user", "content": "eleven"},
]


def test_keeps_everything_when_it_fits():
    assert trim_history(MSGS, 100, count) == MSGS


def test_drops_oldest_first_and_starts_with_user():
    out = trim_history(MSGS, 6, count)
    assert out[-1] == MSGS[-1]
    assert out[0]["role"] == "user"
    assert sum(count(m) for m in out) <= 6


def test_never_drops_the_last_message():
    assert trim_history(MSGS, 0, count) == [MSGS[-1]]
