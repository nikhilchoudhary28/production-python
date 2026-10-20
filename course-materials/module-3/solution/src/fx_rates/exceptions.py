"""Exception hierarchy for foreign exchange rate operations."""


class RateServiceError(Exception):
    """Base class for all FX rate service failures."""
    pass


class RateServiceTimeout(RateServiceError):
    """Raised when the rate service times out (transient)."""
    pass


class RateServiceUnavailable(RateServiceError):
    """Raised when the rate service is temporarily unavailable (transient)."""
    pass


class InvalidCurrencyPairError(RateServiceError):
    """Raised when the requested currency pair is unrecognized (permanent)."""
    pass