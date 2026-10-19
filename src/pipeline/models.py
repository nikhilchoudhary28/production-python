"""Pydantic boundary models for ingesting third-party API records."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class RecordPayload(BaseModel):
    """Nested payload metadata within each API record."""

    channel: Literal["web", "mobile", "pos", "api", "POS"]
    retry_count: int


class IngestionRecord(BaseModel):
    """Validated API record schema enforcing data types at the ingestion boundary."""

    external_id: str
    customer_id: str
    amount: float
    currency: Literal["USD", "EUR", "GBP", "INR", "JPY"]
    status: Literal["completed", "pending", "refunded", "failed"]
    source_created_at: datetime
    source_updated_at: datetime
    payload: RecordPayload