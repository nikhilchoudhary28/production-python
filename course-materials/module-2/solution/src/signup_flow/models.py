"""Domain models for signup processing using Pydantic."""

from datetime import date
from typing import Literal
from pydantic import BaseModel


class SignupRecord(BaseModel):
    """Represents a validated signup payload."""

    email: str
    plan: Literal["free", "pro", "enterprise"]
    signup_date: date
    trial_days: int = 14
    referral_code: str | None = None