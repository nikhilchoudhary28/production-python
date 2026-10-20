"""Generic retry runner configured with exponential backoff and randomized jitter."""

import random
import time
from typing import Callable, TypeVar

from pipeline.exceptions import UpstreamRateLimitError, UpstreamTimeoutError

T = TypeVar("T")

RETRYABLE_EXCEPTIONS = (UpstreamTimeoutError, UpstreamRateLimitError)


def call_with_retry(
    func: Callable[[], T],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 2.0,
) -> T:
    """Executes func with exponential backoff and full jitter.

    Only catches errors in RETRYABLE_EXCEPTIONS.
    Non-retryable errors (e.g., RecordValidationError) bubble up immediately on attempt 1.
    """
    attempt = 0
    while True:
        attempt += 1
        try:
            return func()
        except RETRYABLE_EXCEPTIONS as exc:
            if attempt >= max_attempts:
                raise exc

            # Exponential backoff capped at max_delay
            backoff = min(max_delay, base_delay * (2 ** (attempt - 1)))
            # Full randomized jitter
            delay = random.uniform(0, backoff)

            time.sleep(delay)