def calculate_total(
    unit_price: float, quantity: int, discount_percent: float = 0.0
) -> float:
    """Calculates invoice total with percentage discount applied."""
    subtotal = unit_price * quantity
    discount_amount = subtotal * (discount_percent / 100.0)
    total = subtotal - discount_amount
    return round(total, 2)