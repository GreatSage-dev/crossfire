"""Data models and custom exceptions for CROSSFIRE invariant mining and collision detection."""

from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CrossfireError(Exception):
    """Base exception for all CROSSFIRE errors."""
    pass


class MinerError(CrossfireError):
    """Raised when invariant mining encounters an unrecoverable parsing or extraction error."""
    pass


class DetectorError(CrossfireError):
    """Raised when invariant collision detection fails."""
    pass


class TCASStatus(str, Enum):
    """Tri-State Law (King's Court 3.0 Knot 3): Epistemic refusal over binary thinking.

    - CLEAR: Invariant contracts match deterministically with high confidence (>= 0.70).
    - COLLISION_HALT: Invariant contracts conflict deterministically; execution halted (Exit 2).
    - UNKNOWN_SUSPEND: Claims exhibit ambiguous, dynamic, or low-confidence contracts (< 0.70).
                       The system refuses to guess and suspends execution fail-closed.
    """
    CLEAR = "clear"
    COLLISION_HALT = "collision_halt"
    UNKNOWN_SUSPEND = "unknown_suspend"


class InvariantClaim(BaseModel):
    """Represents a mined invariant claim regarding a symbol's contract or domain.

    Attributes:
        agent_id: Unique identifier for the agent claiming the invariant.
        symbol: The variable, parameter, or symbol name governed by this invariant.
        domain: The value domain or type specification (e.g., 'float[0.0, 1.0]', 'int[0, 100]').
        contract_type: The category of contract: 'value_domain', 'state_lifecycle', or 'error_contract'.
        source_line: 1-indexed line number where the claim was mined from source code.
        confidence: Confidence score of the mined claim, normalized in [0.0, 1.0].
    """

    model_config = ConfigDict(frozen=True)

    agent_id: str = Field(..., description="Unique identifier for the agent or component claiming the invariant.")
    symbol: str = Field(..., description="The variable, parameter, or symbol name governed by this invariant.")
    domain: str = Field(..., description="The value domain or type specification (e.g., 'float[0.0, 1.0]', 'int[0, 100]').")
    contract_type: Literal["value_domain", "state_lifecycle", "error_contract"] = Field(
        ..., description="The architectural category of the invariant contract."
    )
    source_line: int = Field(..., description="1-indexed line number where the claim was mined from source code.")
    confidence: float = Field(..., description="Confidence score of the mined claim, normalized between 0.0 and 1.0.")

    @field_validator("agent_id", "symbol", "domain")
    @classmethod
    def validate_non_empty_strings(cls, value: str, info) -> str:
        """Ensure string fields are non-empty and stripped of surrounding whitespace."""
        if not value or not value.strip():
            raise ValueError(f"Field '{info.field_name}' must not be empty or whitespace only.")
        return value.strip()

    @field_validator("source_line")
    @classmethod
    def validate_source_line(cls, value: int) -> int:
        """Ensure source_line is a positive 1-indexed integer."""
        if value < 1:
            raise ValueError(f"source_line must be >= 1, got {value}")
        return value

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, value: float) -> float:
        """Ensure confidence is normalized between 0.0 and 1.0 inclusive."""
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"confidence must be between 0.0 and 1.0, got {value}")
        return value


class CollisionVector(BaseModel):
    """Represents a detected collision or divergence between two invariant claims.

    Attributes:
        claim_a: The first invariant claim involved in the collision.
        claim_b: The second invariant claim involved in the collision.
        collision_class: Taxonomy class: 'invariant_drift', 'lifecycle_desync', or 'contract_divergence'.
        severity: Estimated severity score between 0.0 (negligible) and 1.0 (catastrophic).
        description: Human and machine-readable explanation of why these claims collide.
        status: Tri-State classification: CLEAR, COLLISION_HALT, or UNKNOWN_SUSPEND.
        epistemic_reason: Optional justification when entering UNKNOWN_SUSPEND (epistemic refusal).
        halted: Flag indicating whether execution should be halted due to this collision.
    """

    model_config = ConfigDict(frozen=True)

    claim_a: InvariantClaim = Field(..., description="The first invariant claim involved in the collision.")
    claim_b: InvariantClaim = Field(..., description="The second invariant claim involved in the collision.")
    collision_class: Literal["invariant_drift", "lifecycle_desync", "contract_divergence"] = Field(
        ..., description="The taxonomy class of the invariant collision."
    )
    severity: float = Field(..., description="Estimated severity score between 0.0 (negligible) and 1.0 (catastrophic).")
    description: str = Field(..., description="Human and machine-readable explanation of why these claims collide.")
    status: TCASStatus = Field(
        default=TCASStatus.COLLISION_HALT,
        description="Tri-State classification: CLEAR, COLLISION_HALT, or UNKNOWN_SUSPEND.",
    )
    epistemic_reason: Optional[str] = Field(
        default=None,
        description="Justification when entering UNKNOWN_SUSPEND (epistemic refusal).",
    )
    halted: bool = Field(default=False, description="Flag indicating whether execution should be halted.")

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: float) -> float:
        """Ensure severity is normalized between 0.0 and 1.0 inclusive."""
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"severity must be between 0.0 and 1.0, got {value}")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        """Ensure description is a non-empty string."""
        if not value or not value.strip():
            raise ValueError("description must not be empty or whitespace only.")
        return value.strip()


class ResolutionAdvisory(BaseModel):
    """Actionable resolution advisory providing remediation guidance for a collision.

    Attributes:
        vector: The collision vector this advisory resolves.
        recommended_action: Actionable recommendation to resolve the collision.
        target_agent: The identifier of the agent that should apply the resolution.
        patch_hint: Code-level or architectural patch recommendation.
    """

    model_config = ConfigDict(frozen=True)

    vector: CollisionVector = Field(..., description="The collision vector this advisory resolves.")
    recommended_action: str = Field(..., description="Actionable recommendation to resolve the collision.")
    target_agent: str = Field(..., description="The identifier of the agent that should apply the resolution.")
    patch_hint: str = Field(..., description="Code-level or architectural patch recommendation.")

    @field_validator("recommended_action", "target_agent", "patch_hint")
    @classmethod
    def validate_non_empty_advisory_fields(cls, value: str, info) -> str:
        """Ensure advisory strings are non-empty."""
        if not value or not value.strip():
            raise ValueError(f"Field '{info.field_name}' must not be empty or whitespace only.")
        return value.strip()
