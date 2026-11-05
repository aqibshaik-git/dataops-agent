import pytest

from dataops_agent.retry import retry


class Flaky:
    def __init__(self, failures, exc=TimeoutError):
        self.failures, self.exc, self.calls = failures, exc, 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.exc("boom")
        return "ok"


def test_succeeds_after_retries_with_full_jitter_backoff():
    slept = []
    f = Flaky(3)
    wrapped = retry(attempts=4, base=0.5, cap=8.0, on=(TimeoutError,), sleep=slept.append, rand=lambda: 1.0)(f)
    assert wrapped() == "ok"
    assert f.calls == 4
    assert slept == [0.5, 1.0, 2.0]


def test_cap_limits_the_wait():
    slept = []
    f = Flaky(5)
    retry(attempts=6, base=1.0, cap=3.0, on=(TimeoutError,), sleep=slept.append, rand=lambda: 1.0)(f)()
    assert slept == [1.0, 2.0, 3.0, 3.0, 3.0]


def test_jitter_scales_the_wait():
    slept = []
    retry(attempts=2, base=2.0, on=(TimeoutError,), sleep=slept.append, rand=lambda: 0.25)(Flaky(1))()
    assert slept == [0.5]


def test_gives_up_and_reraises_last_exception():
    f = Flaky(10)
    with pytest.raises(TimeoutError):
        retry(attempts=3, on=(TimeoutError,), sleep=lambda s: None)(f)()
    assert f.calls == 3


def test_other_exceptions_are_not_retried():
    f = Flaky(1, exc=ValueError)
    with pytest.raises(ValueError):
        retry(attempts=5, on=(TimeoutError,), sleep=lambda s: None)(f)()
    assert f.calls == 1


def test_keeps_name_and_doc():
    @retry(sleep=lambda s: None)
    def fetch_rows():
        """Fetch rows."""
    assert fetch_rows.__name__ == "fetch_rows"
    assert fetch_rows.__doc__ == "Fetch rows."
