"""Subagent A: Gateway Configuration Service.

Assumes timeout is specified in SECONDS (valid range: 1 to 60 seconds).
"""


def configure_gateway(timeout: int = 30) -> dict:
    """Configure network connection parameters with timeout in seconds."""
    assert 1 <= timeout <= 60, "Network gateway timeout must be between 1 and 60 seconds"
    return {"status": "configured", "timeout_sec": timeout}
