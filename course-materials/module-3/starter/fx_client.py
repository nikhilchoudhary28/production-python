"""A simulated third-party FX rate service.

Treat this exactly like a real external API you don't control - read its
behavior by calling it, don't rely on editing it. It's deliberately
flaky in two different ways, on purpose:

- USD/EUR and USD/GBP are temporarily unavailable for their first couple
  of calls, then start working - representing a transient problem
  (think: a timeout, or a 500) that a retry can genuinely fix.
- USD/XXX is not a real currency pair. It will never succeed, no matter
  how many times you call it - representing a permanent problem (think:
  a 400 Bad Request) that no amount of retrying will ever fix.
"""

from exceptions import InvalidCurrencyPairError, RateServiceTimeout, RateServiceUnavailable

_VALID_PAIRS = {"USD/EUR", "USD/GBP", "USD/INR", "USD/JPY"}

# Tracks how many times each pair has been called, so the "flakiness" is
# deterministic and reproducible - not truly random.
_call_counts: dict[str, int] = {}

_RATES = {
    "USD/EUR": 0.92,
    "USD/GBP": 0.79,
    "USD/INR": 83.1,
    "USD/JPY": 149.5,
}


def fetch_rate(pair: str) -> float:
    _call_counts[pair] = _call_counts.get(pair, 0) + 1
    attempt = _call_counts[pair]

    if pair not in _VALID_PAIRS:
        # Always fails. This is not a network problem - the request
        # itself is invalid. Retrying it changes nothing.
        raise InvalidCurrencyPairError(f"{pair} is not a recognized currency pair")

    if pair == "USD/EUR" and attempt < 3:
        raise RateServiceTimeout(f"Timed out fetching {pair} (attempt {attempt})")

    if pair == "USD/GBP" and attempt < 2:
        raise RateServiceUnavailable(f"{pair} service temporarily unavailable")

    return _RATES[pair]


def reset() -> None:
    """Only for re-running the demo from a clean state."""
    _call_counts.clear()
