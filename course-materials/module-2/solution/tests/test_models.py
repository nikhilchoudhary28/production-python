from datetime import date

import pytest
from pydantic import ValidationError

from signup_flow.models import SignupRecord


def valid_signup(**overrides: object) -> SignupRecord:
    data: dict[str, object] = {
        "email": "user@example.com",
        "plan": "pro",
        "signup_date": date(2026, 1, 1),
    }
    data.update(overrides)
    return SignupRecord.model_validate(data)


@pytest.mark.parametrize("bonus_percent", [0, 12.5, 100])
def test_referral_code_with_bonus_is_valid(bonus_percent: float) -> None:
    signup = valid_signup(
        referral_code="WELCOME",
        referral_bonus_percent=bonus_percent,
    )

    assert signup.referral_bonus_percent == bonus_percent


def test_signup_without_referral_code_or_bonus_is_valid() -> None:
    signup = valid_signup()

    assert signup.referral_code is None
    assert signup.referral_bonus_percent is None


@pytest.mark.parametrize(
    "overrides",
    [
        {"referral_code": "WELCOME"},
        {"referral_code": "WELCOME", "referral_bonus_percent": None},
        {"referral_bonus_percent": 10},
        {"referral_bonus_percent": None},
        {"referral_code": "WELCOME", "referral_bonus_percent": -1},
        {"referral_code": "WELCOME", "referral_bonus_percent": 101},
        {"referral_code": "WELCOME", "referral_bonus_percent": "10"},
        {"referral_code": "WELCOME", "referral_bonus_percent": True},
    ],
)
def test_invalid_referral_bonus_combinations_are_rejected(
    overrides: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        valid_signup(**overrides)
