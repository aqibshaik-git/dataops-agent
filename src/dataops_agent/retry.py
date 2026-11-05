"""Fri 13 Nov drill: a retry decorator with exponential back-off and jitter. YOU write it, by hand.

    @retry(attempts=4, base=0.5, cap=8.0, on=(TimeoutError,), sleep=time.sleep, rand=random.random)
    def fetch(): ...

Rules (tests/test_retry.py):
  - Calls the function up to `attempts` times in total. Returns the first successful result.
  - Retries only on exceptions in `on`; anything else is raised immediately.
  - After the last failed attempt, re-raises that attempt's exception.
  - Before retry number n (n = 1, 2, ...): sleep for rand() * min(cap, base * 2 ** (n - 1))   ("full jitter")
  - `sleep` and `rand` are injected so the tests don't wait and are deterministic.
  - functools.wraps: the wrapped function keeps its __name__ and __doc__.
"""
import random
import time


def retry(attempts=3, base=0.5, cap=8.0, on=(Exception,), sleep=time.sleep, rand=random.random):
    raise NotImplementedError
