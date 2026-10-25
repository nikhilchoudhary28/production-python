from invoice_calc import calculate_total


def test_calculate_total_with_discount():
    result = calculate_total(50.0, 10, discount_percent=10)
    assert result == 450.0


def test_calculate_total_with_no_discount():
    result = calculate_total(50.0, 10)
    assert result == 500.0
