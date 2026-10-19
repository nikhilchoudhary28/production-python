"""Domain models for signup processing using Pydantic."""

from datetime import date
from typing import Literal, Self
from pydantic import BaseModel, Field, model_validator


class SignupRecord(BaseModel):
    """Represents a validated signup payload."""

    email: str
    plan: Literal["free", "pro", "enterprise"]
    signup_date: date
    trial_days: int = 14
    referral_code: str | None = None
    referral_bonus_percent: float | None = Field(
        default=None, strict=True, ge=0, le=100
    )

    @model_validator(mode="after")
    def validate_referral_bonus(self) -> Self:
        bonus_was_provided = "referral_bonus_percent" in self.model_fields_set
        if self.referral_code is not None:
            if not bonus_was_provided or self.referral_bonus_percent is None:
                raise ValueError(
                    "referral_bonus_percent is required when referral_code is set"
                )
        elif bonus_was_provided:
            raise ValueError(
                "referral_bonus_percent must not be provided without referral_code"
            )
        return self
