"""TCAS invariant collision detector matching claims across agent boundaries."""

from typing import Optional
from crossfire.models import CollisionVector, DetectorError, InvariantClaim, TCASStatus


def _is_async_domain(domain: str) -> bool:
    """Check if domain represents an asynchronous contract."""
    return "async" in domain.lower()


def _is_sync_domain(domain: str) -> bool:
    """Check if domain represents a synchronous contract."""
    d = domain.lower()
    return "sync" in d and "async" not in d


def _is_none_error_domain(domain: str) -> bool:
    """Check if domain represents returning None/null on error."""
    d = domain.lower()
    return "none" in d or "null" in d


def _is_raise_error_domain(domain: str) -> bool:
    """Check if domain represents raising or catching an exception."""
    d = domain.lower()
    return any(term in d for term in ("raise", "error", "except"))


def _evaluate_tri_state(
    claim_a: InvariantClaim, claim_b: InvariantClaim
) -> tuple[TCASStatus, Optional[str]]:
    """Determine TCAS status under the Tri-State Law (King's Court 3.0 Knot 3).

    Returns (status, epistemic_reason). If confidence < 0.70, the system refuses
    to guess and enters UNKNOWN_SUSPEND fail-closed.
    """
    min_confidence = min(claim_a.confidence, claim_b.confidence)
    if min_confidence < 0.70:
        return (
            TCASStatus.UNKNOWN_SUSPEND,
            f"Epistemic Refusal: Confidence ({min_confidence:.2f}) < 0.70 threshold. "
            "Suspending execution fail-closed to avoid hallucinated contract guessing.",
        )
    return TCASStatus.COLLISION_HALT, None


def detect_collisions(
    claims_a: list[InvariantClaim], claims_b: list[InvariantClaim]
) -> list[CollisionVector]:
    """Detect architectural and contract collisions between two sets of invariant claims.

    Operates under King's Court 3.0 Tri-State Law:
    - CLEAR: Invariant contracts match deterministically with high confidence.
    - COLLISION_HALT: Invariant contracts conflict deterministically (exit code 2).
    - UNKNOWN_SUSPEND: Claims exhibit ambiguous/low-confidence bounds; refuses to guess.
    """
    if not claims_a or not claims_b:
        return []

    try:
        collisions: list[CollisionVector] = []
        symbols_a = {c.symbol for c in claims_a}
        symbols_b = {c.symbol for c in claims_b}
        common_symbols = sorted(symbols_a & symbols_b)

        for symbol in common_symbols:
            c_a_list = [c for c in claims_a if c.symbol == symbol]
            c_b_list = [c for c in claims_b if c.symbol == symbol]

            types_a = {c.contract_type for c in c_a_list}
            types_b = {c.contract_type for c in c_b_list}
            common_types = sorted(types_a & types_b)

            if common_types:
                for ctype in common_types:
                    claim_a = max(
                        [c for c in c_a_list if c.contract_type == ctype],
                        key=lambda c: (c.confidence, -c.source_line),
                    )
                    claim_b = max(
                        [c for c in c_b_list if c.contract_type == ctype],
                        key=lambda c: (c.confidence, -c.source_line),
                    )

                    status, reason = _evaluate_tri_state(claim_a, claim_b)

                    # 1. Value Domain Drift
                    if ctype == "value_domain":
                        if claim_a.domain != claim_b.domain:
                            collisions.append(
                                CollisionVector(
                                    claim_a=claim_a,
                                    claim_b=claim_b,
                                    collision_class="invariant_drift",
                                    severity=0.95,
                                    description=(
                                        f"Value domain drift detected on '{symbol}': "
                                        f"'{claim_a.domain}' ({claim_a.agent_id}) vs "
                                        f"'{claim_b.domain}' ({claim_b.agent_id})"
                                    ),
                                    status=status,
                                    epistemic_reason=reason,
                                    halted=True,
                                )
                            )

                    # 2. State Lifecycle Desync
                    elif ctype == "state_lifecycle":
                        is_async_a = _is_async_domain(claim_a.domain)
                        is_sync_a = _is_sync_domain(claim_a.domain)
                        is_async_b = _is_async_domain(claim_b.domain)
                        is_sync_b = _is_sync_domain(claim_b.domain)

                        if (is_async_a and is_sync_b) or (is_sync_a and is_async_b):
                            collisions.append(
                                CollisionVector(
                                    claim_a=claim_a,
                                    claim_b=claim_b,
                                    collision_class="lifecycle_desync",
                                    severity=0.85,
                                    description=(
                                        f"State lifecycle desync detected on '{symbol}': "
                                        f"'{claim_a.domain}' ({claim_a.agent_id}) vs "
                                        f"'{claim_b.domain}' ({claim_b.agent_id})"
                                    ),
                                    status=status,
                                    epistemic_reason=reason,
                                    halted=True,
                                )
                            )

                    # 3. Error Contract Divergence
                    elif ctype == "error_contract":
                        is_none_a = _is_none_error_domain(claim_a.domain)
                        is_raise_a = _is_raise_error_domain(claim_a.domain)
                        is_none_b = _is_none_error_domain(claim_b.domain)
                        is_raise_b = _is_raise_error_domain(claim_b.domain)

                        if (is_none_a and is_raise_b) or (is_raise_a and is_none_b):
                            collisions.append(
                                CollisionVector(
                                    claim_a=claim_a,
                                    claim_b=claim_b,
                                    collision_class="contract_divergence",
                                    severity=0.90,
                                    description=(
                                        f"Error contract divergence detected on '{symbol}': "
                                        f"'{claim_a.domain}' ({claim_a.agent_id}) vs "
                                        f"'{claim_b.domain}' ({claim_b.agent_id})"
                                    ),
                                    status=status,
                                    epistemic_reason=reason,
                                    halted=True,
                                )
                            )
            else:
                claim_a = max(c_a_list, key=lambda c: (c.confidence, -c.source_line))
                claim_b = max(c_b_list, key=lambda c: (c.confidence, -c.source_line))
                is_none_a = _is_none_error_domain(claim_a.domain)
                is_raise_b = _is_raise_error_domain(claim_b.domain)
                is_none_b = _is_none_error_domain(claim_b.domain)
                is_raise_a = _is_raise_error_domain(claim_a.domain)
                if (is_none_a and is_raise_b) or (is_raise_a and is_none_b):
                    status, reason = _evaluate_tri_state(claim_a, claim_b)
                    collisions.append(
                        CollisionVector(
                            claim_a=claim_a,
                            claim_b=claim_b,
                            collision_class="contract_divergence",
                            severity=0.90,
                            description=(
                                f"Error contract divergence detected on '{symbol}': "
                                f"'{claim_a.domain}' ({claim_a.agent_id}) vs "
                                f"'{claim_b.domain}' ({claim_b.agent_id})"
                            ),
                            status=status,
                            epistemic_reason=reason,
                            halted=True,
                        )
                    )

        return collisions
    except Exception as e:
        if isinstance(e, DetectorError):
            raise
        raise DetectorError(f"Collision detection failed: {e}") from e
