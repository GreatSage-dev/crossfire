"""Agent A: Returns None on missing inventory item."""


def get_item(item_id: str) -> dict | None:
    """Fetches an item by ID, returning None if missing."""
    items = {"item_1": {"name": "Widget"}}
    if item_id not in items:
        return None
    return items[item_id]
