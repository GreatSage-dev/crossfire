"""Unit tests for CROSSFIRE collision detector and TCAS resolution engine."""

from pathlib import Path
import pytest

from crossfire.detector import detect_collisions
from crossfire.miner import extract_claims
from crossfire.models import CollisionVector, InvariantClaim, ResolutionAdvisory
from crossfire.resolver import generate_advisory

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_detect_invariant_drift_value_domain() -> None:
    """Verify detection of value domain drift (float[0.0, 1.0] vs int[0, 100])."""
    source_a = (FIXTURES_DIR / "agent_a_discount.py").read_text(encoding="utf-8")
    source_b = (FIXTURES_DIR / "agent_b_discount.py").read_text(encoding="utf-8")

    claims_a = extract_claims(source_a, agent_id="agent_a")
    claims_b = extract_claims(source_b, agent_id="agent_b")

    collisions = detect_collisions(claims_a, claims_b)

    assert len(collisions) >= 1
    drift_collisions = [c for c in collisions if c.collision_class == "invariant_drift"]
    assert len(drift_collisions) >= 1

    col = drift_collisions[0]
    assert col.severity >= 0.90
    assert col.halted is True
    assert col.claim_a.symbol == "discount"

    # Test resolution advisory generation
    advisory = generate_advisory(col)
    assert isinstance(advisory, ResolutionAdvisory)
    assert advisory.target_agent in ("agent_a", "agent_b")
    assert "discount" in advisory.recommended_action.lower()
    assert "100" in advisory.patch_hint or "float" in advisory.patch_hint


def test_detect_lifecycle_desync() -> None:
    """Verify detection of state lifecycle desync (async coroutine vs sync function)."""
    source_a = (FIXTURES_DIR / "agent_a_lifecycle.py").read_text(encoding="utf-8")
    source_b = (FIXTURES_DIR / "agent_b_lifecycle.py").read_text(encoding="utf-8")

    claims_a = extract_claims(source_a, agent_id="agent_a")
    claims_b = extract_claims(source_b, agent_id="agent_b")

    collisions = detect_collisions(claims_a, claims_b)

    assert len(collisions) >= 1
    sync_collisions = [c for c in collisions if c.collision_class == "lifecycle_desync"]
    assert len(sync_collisions) >= 1

    col = sync_collisions[0]
    assert col.severity >= 0.80
    assert col.halted is True

    # Test resolution advisory generation
    advisory = generate_advisory(col)
    assert isinstance(advisory, ResolutionAdvisory)
    assert "async" in advisory.recommended_action.lower()


def test_detect_contract_divergence_error() -> None:
    """Verify detection of error contract divergence (return None vs raise exception)."""
    source_a = (FIXTURES_DIR / "agent_a_error.py").read_text(encoding="utf-8")
    source_b = (FIXTURES_DIR / "agent_b_error.py").read_text(encoding="utf-8")

    claims_a = extract_claims(source_a, agent_id="agent_a")
    claims_b = extract_claims(source_b, agent_id="agent_b")

    collisions = detect_collisions(claims_a, claims_b)

    assert len(collisions) >= 1
    error_collisions = [c for c in collisions if c.collision_class == "contract_divergence"]
    assert len(error_collisions) >= 1

    col = error_collisions[0]
    assert col.severity >= 0.85
    assert col.halted is True

    # Test resolution advisory generation
    advisory = generate_advisory(col)
    assert isinstance(advisory, ResolutionAdvisory)
    assert "none" in advisory.patch_hint.lower() or "raise" in advisory.patch_hint.lower()


def test_clean_claims_produce_no_collisions() -> None:
    """Verify that matching claims on identical domains produce zero collisions."""
    claim_1 = InvariantClaim(
        agent_id="agent_a",
        symbol="rate",
        domain="float[0.0, 1.0]",
        contract_type="value_domain",
        source_line=10,
        confidence=1.0,
    )
    claim_2 = InvariantClaim(
        agent_id="agent_b",
        symbol="rate",
        domain="float[0.0, 1.0]",
        contract_type="value_domain",
        source_line=12,
        confidence=1.0,
    )

    collisions = detect_collisions([claim_1], [claim_2])
    assert len(collisions) == 0


def test_empty_claims_produce_no_collisions() -> None:
    """Verify that empty claim lists produce zero collisions without error."""
    assert detect_collisions([], []) == []
    claim = InvariantClaim(
        agent_id="agent_a",
        symbol="test",
        domain="int[0, 10]",
        contract_type="value_domain",
        source_line=1,
        confidence=0.9,
    )
    assert detect_collisions([claim], []) == []
    assert detect_collisions([], [claim]) == []
