"""A simulated report database. You don't need to edit this file.

Notice what it does when the password is wrong: it doesn't raise an
error. It quietly returns a different, smaller dataset instead - the
same way a real misconfigured connection might silently land you on
the wrong environment instead of failing loudly.
"""

_REAL_PASSWORD = "vault-injected-prod-secret-9f3a"

_REAL_REVENUE_TOTALS = {"Q1": 482_910.00, "Q2": 511_204.50, "Q3": 498_775.25}
_WRONG_ENVIRONMENT_TOTALS = {"Q1": 1_200.00, "Q2": 980.50, "Q3": 1_450.75}


def fetch_quarterly_revenue(host: str, password: str) -> dict[str, float]:
    if password == _REAL_PASSWORD:
        return dict(_REAL_REVENUE_TOTALS)
    # Wrong password - but instead of refusing to connect, this
    # simulates landing on some other, wrong environment entirely.
    # No error. No warning. Just quietly wrong numbers.
    return dict(_WRONG_ENVIRONMENT_TOTALS)
