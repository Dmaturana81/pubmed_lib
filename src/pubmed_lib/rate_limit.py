"""NCBI Entrez rate limiting."""

from __future__ import annotations

import time
from threading import Lock

MAX_RESULTS_HARD_CAP = 200


def validate_max_results(max_results: int) -> int:
    """Validate and return max_results within allowed bounds."""
    if max_results < 1:
        raise ValueError("max_results must be at least 1")
    if max_results > MAX_RESULTS_HARD_CAP:
        raise ValueError(f"max_results cannot exceed {MAX_RESULTS_HARD_CAP}")
    return max_results


class RateLimiter:
    """Thread-safe delay between Entrez requests."""

    def __init__(self, *, has_api_key: bool) -> None:
        self._min_interval = 1.0 / 3.0 if has_api_key else 10.0 / 3.0
        self._lock = Lock()
        self._last_request = 0.0

    def acquire(self) -> None:
        """Wait until the next Entrez request is allowed."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_request
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
            self._last_request = time.monotonic()
