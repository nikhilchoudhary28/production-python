class RateServiceError(Exception):
    """Base class for anything that can go wrong calling the FX service."""


class RateServiceTimeout(RateServiceError):
    """The service didn't respond in time. Transient - retrying can help."""


class RateServiceUnavailable(RateServiceError):
    """The service is temporarily down. Transient - retrying can help."""


class InvalidCurrencyPairError(RateServiceError):
    """The requested pair doesn't exist. Permanent - retrying never helps."""
