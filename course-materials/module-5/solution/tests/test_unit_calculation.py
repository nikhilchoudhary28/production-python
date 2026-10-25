"""Unit tests - the pure calculation logic, no database involved at all."""

from discounts.discount import compute_discounted_total


def test_applies_percentage_discount() -> None:
    assert compute_discounted_total(100.0, 10.0) == 90.0


def test_zero_discount_leaves_total_unchanged() -> None:
    assert compute_discounted_total(100.0, 0.0) == 100.0


def test_full_discount_gives_zero() -> None:
    assert compute_discounted_total(100.0, 100.0) == 0.0


def test_rounds_to_two_decimal_places() -> None:
    assert compute_discounted_total(19.99, 15.0) == 16.99
