"""Classified exception hierarchy for the capstone ingestion service."""


class IngestionError(Exception):
    """Base exception for all pipeline ingestion failures."""


class UpstreamTimeoutError(IngestionError):
    """Raised when the mock API times out (transient, retryable)."""


class UpstreamRateLimitError(IngestionError):
    """Raised when the mock API returns HTTP 429 rate limit (transient, retryable)."""


class RecordValidationError(IngestionError):
    """Raised when incoming data fails Pydantic boundary validation (permanent, non-retryable)."""
