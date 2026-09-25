"""Agent B: Raises ItemNotFoundError on missing inventory item."""


class ItemNotFoundError(Exception):
    """Raised when an item is not found in inventory."""
    pass


def get_item(item_id: str) -> dict:
    """Fetches an item by ID, raising ItemNotFoundError if missing."""
    items = {"item_1": {"name": "Widget"}}
    if item_id not in items:
        raise ItemNotFoundError(f"Item {item_id} not found")
    return items[item_id]
