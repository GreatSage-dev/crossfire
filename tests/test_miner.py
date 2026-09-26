"""Unit tests for CROSSFIRE AST invariant claim miner and domain contracts."""

from pathlib import Path
import pytest
from pydantic import ValidationError

from crossfire.miner import extract_claims
from crossfire.models import (
    CollisionVector,
    CrossfireError,
    DetectorError,
    InvariantClaim,
    MinerError,
    ResolutionAdvisory,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_extract_claims_agent_a() -> None:
    """Verify claim extraction on agent A fixture enforcing float[0.0, 1.0]."""
    source_path = FIXTURES_DIR / "agent_a_discount.py"
    source = source_path.read_text(encoding="utf-8")

    claims = extract_claims(source, agent_id="agent_a")

    assert len(claims) >= 3, f"Expected at least 3 claims, found {len(claims)}"

    for claim in claims:
        assert isinstance(claim, InvariantClaim)
        assert claim.agent_id == "agent_a"
        assert claim.contract_type == "value_domain"
        assert claim.domain == "float[0.0, 1.0]"
        assert 0.0 <= claim.confidence <= 1.0

    # Ensure the assertion claim at line 6 is captured with maximum confidence
    assertion_claims = [c for c in claims if c.source_line == 6 and c.symbol == "discount"]
    assert len(assertion_claims) == 1
    assert assertion_claims[0].confidence == 1.0
    assert assertion_claims[0].domain == "float[0.0, 1.0]"

    # Ensure default argument claim is captured
    default_claims = [c for c in claims if c.source_line == 4 and c.symbol == "discount"]
    assert len(default_claims) == 1
    assert default_claims[0].domain == "float[0.0, 1.0]"


def test_extract_claims_agent_b() -> None:
    """Verify claim extraction on agent B fixture expecting int[0, 100]."""
    source_path = FIXTURES_DIR / "agent_b_discount.py"
    source = source_path.read_text(encoding="utf-8")

    claims = extract_claims(source, agent_id="agent_b")

    assert len(claims) >= 3, f"Expected at least 3 claims, found {len(claims)}"

    for claim in claims:
        assert isinstance(claim, InvariantClaim)
        assert claim.agent_id == "agent_b"
        assert claim.contract_type == "value_domain"
        assert 0.0 <= claim.confidence <= 1.0

    # All discount-related claims must assert int[0, 100]
    discount_claims = [c for c in claims if c.symbol == "discount"]
    assert len(discount_claims) >= 2
    for claim in discount_claims:
        assert claim.domain == "int[0, 100]"

    # Check assertion claim at line 6
    assertion_claims = [c for c in claims if c.source_line == 6 and c.symbol == "discount"]
    assert len(assertion_claims) == 1
    assert assertion_claims[0].confidence == 1.0
    assert assertion_claims[0].domain == "int[0, 100]"


def test_domain_divergence_between_agents() -> None:
    """Verify that agent_a and agent_b claims diverge on symbol 'discount'."""
    src_a = (FIXTURES_DIR / "agent_a_discount.py").read_text(encoding="utf-8")
    src_b = (FIXTURES_DIR / "agent_b_discount.py").read_text(encoding="utf-8")

    claims_a = extract_claims(src_a, agent_id="agent_a")
    claims_b = extract_claims(src_b, agent_id="agent_b")

    discount_a = [c for c in claims_a if c.symbol == "discount"][0]
    discount_b = [c for c in claims_b if c.symbol == "discount"][0]

    assert discount_a.domain != discount_b.domain
    assert discount_a.domain == "float[0.0, 1.0]"
    assert discount_b.domain == "int[0, 100]"

    # Construct collision vector
    vector = CollisionVector(
        claim_a=discount_a,
        claim_b=discount_b,
        collision_class="contract_divergence",
        severity=0.9,
        description=f"Domain mismatch on 'discount': {discount_a.domain} vs {discount_b.domain}",
    )
    assert vector.severity == 0.9
    assert vector.halted is False

    # Construct resolution advisory
    advisory = ResolutionAdvisory(
        vector=vector,
        recommended_action="Normalize discount input in Agent B to float in [0.0, 1.0]",
        target_agent="agent_b",
        patch_hint="discount = float(discount) / 100.0 if discount > 1.0 else float(discount)",
    )
    assert advisory.target_agent == "agent_b"


def test_syntax_error_raises_miner_error() -> None:
    """Verify that invalid Python syntax triggers MinerError."""
    malformed_source = "def broken_code(x:\n  return x +"
    with pytest.raises(MinerError) as exc_info:
        extract_claims(malformed_source, agent_id="malformed_agent")
    assert "Failed to parse source code" in str(exc_info.value)


def test_empty_source_returns_empty_list() -> None:
    """Verify empty or whitespace-only code returns an empty list without error."""
    assert extract_claims("", agent_id="empty") == []
    assert extract_claims("   \n\t  ", agent_id="empty") == []


def test_custom_exception_hierarchy() -> None:
    """Verify custom exception inheritance hierarchy."""
    assert issubclass(MinerError, CrossfireError)
    assert issubclass(DetectorError, CrossfireError)
    assert issubclass(CrossfireError, Exception)


def test_comparison_chain_variations() -> None:
    """Verify detection on descending chains and boolop assertions."""
    source = """
assert 1.0 >= rate >= 0.0
assert rate >= 0.0 and rate <= 1.0
assert margin <= 100
"""
    claims = extract_claims(source, agent_id="test_agent")
    rate_claims = [c for c in claims if c.symbol == "rate"]
    assert any(c.domain == "float[0.0, 1.0]" for c in rate_claims)

    margin_claims = [c for c in claims if c.symbol == "margin"]
    assert any(c.domain == "int[0, 100]" for c in margin_claims)


def test_literal_percentage_multiplication() -> None:
    """Verify detection of literal percentage multiplications."""
    source = """
def compute(price: float) -> float:
    disc_a = price * 0.15
    disc_b = price * 15
    return disc_a
"""
    claims = extract_claims(source, agent_id="agent_math")
    domains = {c.domain for c in claims}
    assert "float[0.0, 1.0]" in domains
    assert "int[0, 100]" in domains


def test_pydantic_model_validators() -> None:
    """Verify Pydantic v2 validation logic across models."""
    valid_claim = InvariantClaim(
        agent_id="agent_test",
        symbol="discount",
        domain="float[0.0, 1.0]",
        contract_type="value_domain",
        source_line=10,
        confidence=0.95,
    )
    assert valid_claim.symbol == "discount"

    # Invalid confidence > 1.0
    with pytest.raises(ValidationError):
        InvariantClaim(
            agent_id="agent_test",
            symbol="discount",
            domain="float[0.0, 1.0]",
            contract_type="value_domain",
            source_line=1,
            confidence=1.5,
        )

    # Invalid source_line < 1
    with pytest.raises(ValidationError):
        InvariantClaim(
            agent_id="agent_test",
            symbol="discount",
            domain="float[0.0, 1.0]",
            contract_type="value_domain",
            source_line=0,
            confidence=0.8,
        )

    # Empty symbol
    with pytest.raises(ValidationError):
        InvariantClaim(
            agent_id="agent_test",
            symbol="   ",
            domain="float[0.0, 1.0]",
            contract_type="value_domain",
            source_line=1,
            confidence=0.8,
        )

    # Invalid contract_type
    with pytest.raises(ValidationError):
        InvariantClaim(
            agent_id="agent_test",
            symbol="discount",
            domain="float[0.0, 1.0]",
            contract_type="invalid_type",  # type: ignore[arg-type]
            source_line=1,
            confidence=0.8,
        )


def test_extract_claims_arbitrary_unseen_symbols() -> None:
    """Verify that miner extracts invariant claims on arbitrary user-defined symbols (no hardcoding)."""
    source_code = """
def update_liquidity_pool(token_ratio: float = 0.25):
    assert 0.0 <= token_ratio <= 1.0
    fee_percentage = 20
    return token_ratio * 100
"""
    claims = extract_claims(source_code, agent_id="agent_quant")
    symbols = {c.symbol: c.domain for c in claims}

    # token_ratio must have float[0.0, 1.0] extracted from assertion and parameter default
    token_claims = [c for c in claims if c.symbol == "token_ratio"]
    assert any(c.domain == "float[0.0, 1.0]" for c in token_claims)

    # fee_percentage must be extracted as int[0, 100] from constant assignment
    fee_claims = [c for c in claims if c.symbol == "fee_percentage"]
    assert any(c.domain == "int[0, 100]" for c in fee_claims)

