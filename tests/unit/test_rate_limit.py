"""Rate limiter tests."""

import time

import pytest

from pubmed_lib.rate_limit import RateLimiter, validate_max_results


def test_validate_max_results_rejects_over_cap() -> None:
    with pytest.raises(ValueError, match="200"):
        validate_max_results(201)


def test_rate_limiter_enforces_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    clock = iter([0.0, 0.1, 0.2])
    sleeps: list[float] = []
    monkeypatch.setattr(time, "monotonic", lambda: next(clock, 10.0))
    monkeypatch.setattr(time, "sleep", lambda seconds: sleeps.append(seconds))
    limiter = RateLimiter(has_api_key=False)
    limiter.acquire()
    limiter.acquire()
    assert sleeps and sleeps[0] > 0
