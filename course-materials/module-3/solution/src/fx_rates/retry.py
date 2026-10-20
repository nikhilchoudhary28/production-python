"""Generic retry runner with exponential backoff and randomized jitter."""

import random
import time
from typing import Callable, TypeVar

from fx_rates.exceptions import RateServiceTimeout, RateServiceUnavailable

T = TypeVar("T")

RETRYABLE_EXCEPTIONS = (RateServiceTimeout, RateServiceUnavailable)


def call_with_retry(
    func: Callable[[], T],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 2.0,
) -> T:
    """Executes a zero-argument callable with exponential backoff and jitter."""
    attempt = 0
    while True:
        attempt += 1
        try:
            return func()
        except RETRYABLE_EXCEPTIONS as exc:
            if attempt >= max_attempts:
                raise exc

            backoff = min(max_delay, base_delay * (2 ** (attempt - 1)))
            delay = random.uniform(0, backoff)

            print(f"  attempt {attempt} failed ({exc}), retrying in {delay:.3f}s...")
            time.sleep(delay)