"""Rate fetcher integrating the FX client with generic retry policies."""

from fx_rates.fx_client import fetch_rate
from fx_rates.retry import call_with_retry


def get_rate(pair: str) -> float:
    """Fetches exchange rate for a pair using call_with_retry."""
    return call_with_retry(lambda: fetch_rate(pair))