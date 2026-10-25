from invoice_calc import calculate_total


def test_calculate_total_with_discount() -> None:
    result = calculate_total(50.0, 10, discount_percent=10.0)
    assert result == 450.0


def test_calculate_total_with_no_discount() -> None:
    result = calculate_total(50.0, 10)
    assert result == 500.0


def test_calculate_total_zero_quantity() -> None:
    result = calculate_total(50.0, 0, discount_percent=10.0)
    assert result == 0.0
