import time

from exceptions import RateServiceError
from fx_client import fetch_rate


def get_rate_with_retry(pair: str, max_attempts: int = 5) -> float:
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        try:
            return fetch_rate(pair)
        except RateServiceError as e:
            print(f"  attempt {attempts} failed: {e}")
            time.sleep(0.1)
    raise RuntimeError(f"Failed to fetch rate for {pair} after {max_attempts} attempts")
