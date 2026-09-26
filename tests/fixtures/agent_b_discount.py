"""Agent B: Calculates discounts using integer percentage domain [0, 100]."""


def calculate_promotional_price(price: float, discount: int = 15) -> float:
    """Calculate discounted price using integer percentage domain [0, 100]."""
    assert 0 <= discount <= 100, "Discount percentage must be between 0 and 100"
    return price * (1.0 - discount / 100.0)


def place_order_with_promotion(price: float) -> float:
    """Passes integer percentage 15 expecting [0, 100] domain."""
    selected_discount = 15
    return calculate_promotional_price(price, discount=15)
