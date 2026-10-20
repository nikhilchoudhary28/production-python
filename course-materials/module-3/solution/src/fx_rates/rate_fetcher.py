"""Rate fetcher integrating the FX client with generic retry policies."""

from fx_rates.fx_client import fetch_historical_rate, fetch_rate
from fx_rates.retry import call_with_retry


def get_rate(pair: str) -> float:
    """Fetches exchange rate for a pair using call_with_retry."""
    return call_with_retry(lambda: fetch_rate(pair))


def get_historical_rate(pair: str, date: str) -> float:
    """Fetches a historical exchange rate for a pair using call_with_retry."""
    return call_with_retry(lambda: fetch_historical_rate(pair, date))