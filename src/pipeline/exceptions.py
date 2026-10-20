"""Classified exception hierarchy for the capstone ingestion service."""


class IngestionError(Exception):
    """Base exception for all pipeline ingestion failures."""
    pass


class UpstreamTimeoutError(IngestionError):
    """Raised when the mock API times out (transient, retryable)."""
    pass


class UpstreamRateLimitError(IngestionError):
    """Raised when the mock API returns HTTP 429 rate limit (transient, retryable)."""
    pass


class RecordValidationError(IngestionError):
    """Raised when incoming data fails Pydantic boundary validation (permanent, non-retryable)."""
    pass