"""Agent B: Calculates discounts using normalized float domain [0.0, 1.0]."""


def calculate_promotional_price(price: float, discount: float = 0.15) -> float:
    """Calculate discounted price using normalized float domain [0.0, 1.0].

    TCAS Advisory applied: integer percentage domain [0, 100] converted to
    float [0.0, 1.0] to align with Agent A's invariant contract on 'discount'.
    """
    # TCAS Patch: normalize integer percentage to float domain if needed
    discount = float(discount) / 100.0 if discount > 1.0 else float(discount)
    assert 0.0 <= discount <= 1.0, "Discount must be normalized between 0.0 and 1.0"
    return price * (1.0 - discount)


def place_order_with_promotion(price: float) -> float:
    """Passes normalized float 0.15 aligned to [0.0, 1.0] domain."""
    selected_discount = 0.15
    return calculate_promotional_price(price, discount=0.15)
