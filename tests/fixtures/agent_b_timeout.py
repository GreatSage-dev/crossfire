"""Subagent B: Client Initialization Service.

Assumes timeout is specified in MILLISECONDS (passes 5000 ms for 5-second timeout).
Type checker sees int -> int: 100% valid!
"""


def initialize_client() -> dict:
    """Initialize client connection assuming millisecond timeout convention."""
    timeout: int = 5000
    # Calls configure_gateway with integer 5000 (expecting ms)
    return {"client": "ready", "timeout": timeout}
