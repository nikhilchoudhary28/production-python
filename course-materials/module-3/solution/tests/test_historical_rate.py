import pytest

import fx_rates.fx_client as fx_client
import fx_rates.retry as retry
from fx_rates.exceptions import InvalidCurrencyPairError
from fx_rates.rate_fetcher import get_historical_rate


def test_get_historical_rate_retries_transient_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fx_client.reset()
    monkeypatch.setattr(retry.time, "sleep", lambda _delay: None)

    try:
        assert get_historical_rate("USD/EUR", "2025-01-01") == 0.92
        assert fx_client._call_counts["USD/EUR"] == 3
    finally:
        fx_client.reset()


def test_get_historical_rate_does_not_retry_invalid_pair() -> None:
    fx_client.reset()

    try:
        with pytest.raises(InvalidCurrencyPairError):
            get_historical_rate("USD/XXX", "2025-01-01")

        assert fx_client._call_counts["USD/XXX"] == 1
    finally:
        fx_client.reset()
