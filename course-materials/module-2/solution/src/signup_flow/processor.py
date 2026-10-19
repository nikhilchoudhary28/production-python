"""Processing calculations that operate on validated SignupRecord models."""

from datetime import timedelta
from signup_flow.models import SignupRecord


def compute_trial_end_dates(records: list[SignupRecord]) -> list[dict[str, str]]:
    """Calculates trial end date for each validated signup record."""
    results: list[dict[str, str]] = []
    for record in records:
        trial_end = record.signup_date + timedelta(days=record.trial_days)
        results.append(
            {
                "email": record.email,
                "plan": record.plan,
                "trial_end": trial_end.isoformat(),
            }
        )
    return results


def count_by_plan(records: list[SignupRecord]) -> dict[str, int]:
    """Aggregates signup counts grouped by plan tier."""
    counts: dict[str, int] = {}
    for record in records:
        counts[record.plan] = counts.get(record.plan, 0) + 1
    return counts