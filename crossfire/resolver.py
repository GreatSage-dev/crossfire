"""TCAS Resolution Advisory generator for automated collision steering."""

import re
from crossfire.models import CollisionVector, ResolutionAdvisory


def _extract_exc_name(domain: str) -> str:
    """Extract exception class name from domain string."""
    match = re.search(r"raises\[([A-Za-z0-9_]+)\]", domain)
    if match:
        return match.group(1)
    match = re.search(r"raise\s+([A-Za-z0-9_]+)", domain, re.IGNORECASE)
    if match:
        return match.group(1)
    return "ItemNotFoundError"


def generate_advisory(vector: CollisionVector) -> ResolutionAdvisory:
    """Generate an actionable, imperative TCAS Resolution Advisory with an exact patch hint.

    Advisories are modeled after aviation TCAS resolution maneuvers (e.g., 'CLIMB', 'DESCEND'):
    they provide imperative steering instructions and explicit patch hints targeted at the
    agent requiring remediation.

    Args:
        vector: Detected CollisionVector requiring resolution.

    Returns:
        ResolutionAdvisory containing the remediation recommendation, target agent, and patch hint.
    """
    collision_class = vector.collision_class

    if collision_class == "invariant_drift":
        # Check which claim has integer percentage domain
        if "int" in vector.claim_b.domain.lower():
            target_agent = vector.claim_b.agent_id
            symbol = vector.claim_b.symbol
            recommended_action = f"Normalize {symbol} in {target_agent} to float domain [0.0, 1.0]"
            patch_hint = f"{symbol} = float({symbol}) / 100.0 if {symbol} > 1.0 else float({symbol})"
        elif "int" in vector.claim_a.domain.lower():
            target_agent = vector.claim_a.agent_id
            symbol = vector.claim_a.symbol
            recommended_action = f"Normalize {symbol} in {target_agent} to float domain [0.0, 1.0]"
            patch_hint = f"{symbol} = float({symbol}) / 100.0 if {symbol} > 1.0 else float({symbol})"
        else:
            target_agent = vector.claim_b.agent_id
            symbol = vector.claim_b.symbol
            recommended_action = f"Align value domain of '{symbol}' in {target_agent} to '{vector.claim_a.domain}'"
            patch_hint = f"# TCAS Patch: align domain of {symbol} to {vector.claim_a.domain}"

    elif collision_class == "lifecycle_desync":
        # Target the synchronous component to convert or wrap as async
        if "sync" in vector.claim_b.domain.lower() and "async" not in vector.claim_b.domain.lower():
            target_agent = vector.claim_b.agent_id
            symbol = vector.claim_b.symbol
            recommended_action = (
                f"Migrate synchronous {symbol} in {target_agent} to async coroutine to prevent event loop blocking"
            )
            patch_hint = (
                f"async def {symbol}(*args, **kwargs):\n"
                f"    # TCAS Advisory: Converted synchronous blocking call to async coroutine\n"
                f"    ..."
            )
        elif "sync" in vector.claim_a.domain.lower() and "async" not in vector.claim_a.domain.lower():
            target_agent = vector.claim_a.agent_id
            symbol = vector.claim_a.symbol
            recommended_action = (
                f"Migrate synchronous {symbol} in {target_agent} to async coroutine to prevent event loop blocking"
            )
            patch_hint = (
                f"async def {symbol}(*args, **kwargs):\n"
                f"    # TCAS Advisory: Converted synchronous blocking call to async coroutine\n"
                f"    ..."
            )
        else:
            target_agent = vector.claim_b.agent_id
            symbol = vector.claim_b.symbol
            recommended_action = f"Reconcile lifecycle execution model for '{symbol}' in {target_agent}"
            patch_hint = f"# TCAS Advisory: Ensure {symbol} matches async coroutine lifecycle"

    elif collision_class == "contract_divergence":
        # Target the agent returning None to raise an explicit exception
        is_none_b = "none" in vector.claim_b.domain.lower() or "null" in vector.claim_b.domain.lower()
        if is_none_b:
            target_agent = vector.claim_b.agent_id
            symbol = vector.claim_b.symbol
            exc_name = _extract_exc_name(vector.claim_a.domain)
            recommended_action = f"Update {symbol} in {target_agent} to raise {exc_name} instead of returning None"
            patch_hint = f"if not result:\n    raise {exc_name}(f'{symbol} not found')"
        else:
            target_agent = vector.claim_a.agent_id
            symbol = vector.claim_a.symbol
            exc_name = _extract_exc_name(vector.claim_b.domain)
            recommended_action = f"Update {symbol} in {target_agent} to raise {exc_name} instead of returning None"
            patch_hint = f"if not result:\n    raise {exc_name}(f'{symbol} not found')"

    else:
        target_agent = vector.claim_b.agent_id
        symbol = vector.claim_b.symbol
        recommended_action = f"Reconcile contract mismatch on '{symbol}'"
        patch_hint = f"# TCAS Advisory: reconcile contract on {symbol}"

    return ResolutionAdvisory(
        vector=vector,
        recommended_action=recommended_action,
        target_agent=target_agent,
        patch_hint=patch_hint,
    )
