"""Agent A: Calculates discounts assuming discount rate is normalized to float [0.0, 1.0]."""


def calculate_discounted_price(price: float, discount: float = 0.15) -> float:
    """Apply discount rate to price, enforcing normalized float domain [0.0, 1.0]."""
    assert 0.0 <= discount <= 1.0, "Discount must be normalized between 0.0 and 1.0"
    base_deduction = price * 0.15
    return price * (1.0 - discount)
