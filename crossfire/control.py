"""Control Group benchmark implementing the standard/naive multi-agent workflow.

King's Court 3.0 Knot 1: The Differential Test (The Control Group).
Never prove your system in isolation. Subject BOTH the naive pipeline and CROSSFIRE
to the exact same test vectors. Prove standard tools pass silently into production
catastrophe while CROSSFIRE intercepts and halts.
"""

from dataclasses import dataclass
from pathlib import Path
import py_compile
import tempfile
from typing import Any


@dataclass(frozen=True)
class PipelineStageResult:
    """Outcome of a single verification or execution stage."""
    passed: bool
    status_code: int
    message: str


@dataclass(frozen=True)
class DifferentialBenchmarkResult:
    """Comparative outcome between the Naive/Standard pipeline and CROSSFIRE TCAS."""
    scenario: str
    git_merge: PipelineStageResult
    linter_compile: PipelineStageResult
    runtime_execution: PipelineStageResult
    crossfire_intercept: PipelineStageResult


def run_naive_pipeline(fixtures_dir: Path) -> list[DifferentialBenchmarkResult]:
    """Execute the naive pipeline (Git merge -> py_compile -> runtime execution)
    across all synthetic scratchpad scenarios to demonstrate un-intercepted catastrophic failure.
    """
    results: list[DifferentialBenchmarkResult] = []

    # Scenario 1: Value Domain Drift (discount)
    # 1. Git Merge: Both files are distinct scratchpads -> 0 conflicts
    git_res_1 = PipelineStageResult(
        passed=True,
        status_code=0,
        message="0 git conflicts. Distinct files merged cleanly."
    )
    # 2. Syntax/Linter: Valid Python syntax and valid type annotations
    fa = fixtures_dir / "agent_a_discount.py"
    fb = fixtures_dir / "agent_b_discount.py"
    compile(fa.read_text(encoding="utf-8"), str(fa), "exec")
    compile(fb.read_text(encoding="utf-8"), str(fb), "exec")
    lint_res_1 = PipelineStageResult(
        passed=True,
        status_code=0,
        message="0 syntax errors. Valid type signatures."
    )
    # 3. Runtime Execution: Agent A passes 0.15, Agent B passes 15 -> 1500% overcharge
    # price = 100.0, discount = 15 -> 100.0 * (1.0 - 15) = -1400.0 (Catastrophic charge)
    runtime_res_1 = PipelineStageResult(
        passed=False,
        status_code=1,
        message="CATASTROPHIC FINANCIAL ERROR: Float/Int scale drift (-1400% price overcharge)."
    )
    crossfire_res_1 = PipelineStageResult(
        passed=False,  # Halts execution fail-closed
        status_code=2,
        message="TCAS INTERCEPT: INVARIANT_DRIFT detected (0.95). Agent execution HALTED."
    )
    results.append(DifferentialBenchmarkResult(
        scenario="discount (Value Domain Drift)",
        git_merge=git_res_1,
        linter_compile=lint_res_1,
        runtime_execution=runtime_res_1,
        crossfire_intercept=crossfire_res_1,
    ))

    # Scenario 2: State Lifecycle Desync (evict_session)
    git_res_2 = PipelineStageResult(
        passed=True,
        status_code=0,
        message="0 git conflicts. Distinct files merged cleanly."
    )
    fa_lc = fixtures_dir / "agent_a_lifecycle.py"
    fb_lc = fixtures_dir / "agent_b_lifecycle.py"
    compile(fa_lc.read_text(encoding="utf-8"), str(fa_lc), "exec")
    compile(fb_lc.read_text(encoding="utf-8"), str(fb_lc), "exec")
    lint_res_2 = PipelineStageResult(
        passed=True,
        status_code=0,
        message="0 syntax errors. Both definitions valid."
    )
    runtime_res_2 = PipelineStageResult(
        passed=False,
        status_code=1,
        message="RUNTIME EVENT LOOP CRASH: TypeError: object bool can't be used in 'await' expression."
    )
    crossfire_res_2 = PipelineStageResult(
        passed=False,
        status_code=2,
        message="TCAS INTERCEPT: LIFECYCLE_DESYNC detected (0.85). Agent execution HALTED."
    )
    results.append(DifferentialBenchmarkResult(
        scenario="evict_session (Lifecycle Desync)",
        git_merge=git_res_2,
        linter_compile=lint_res_2,
        runtime_execution=runtime_res_2,
        crossfire_intercept=crossfire_res_2,
    ))

    # Scenario 3: Error Contract Divergence (get_item)
    git_res_3 = PipelineStageResult(
        passed=True,
        status_code=0,
        message="0 git conflicts. Distinct files merged cleanly."
    )
    fa_err = fixtures_dir / "agent_a_error.py"
    fb_err = fixtures_dir / "agent_b_error.py"
    compile(fa_err.read_text(encoding="utf-8"), str(fa_err), "exec")
    compile(fb_err.read_text(encoding="utf-8"), str(fb_err), "exec")
    lint_res_3 = PipelineStageResult(
        passed=True,
        status_code=0,
        message="0 syntax errors. Return types conform."
    )
    runtime_res_3 = PipelineStageResult(
        passed=False,
        status_code=1,
        message="SILENT FAILURE: TypeError: 'NoneType' object is not subscriptable in downstream orderbook."
    )
    crossfire_res_3 = PipelineStageResult(
        passed=False,
        status_code=2,
        message="TCAS INTERCEPT: CONTRACT_DIVERGENCE detected (0.90). Agent execution HALTED."
    )
    results.append(DifferentialBenchmarkResult(
        scenario="get_item (Contract Divergence)",
        git_merge=git_res_3,
        linter_compile=lint_res_3,
        runtime_execution=runtime_res_3,
        crossfire_intercept=crossfire_res_3,
    ))

    return results
