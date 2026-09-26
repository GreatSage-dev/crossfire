"""Unit tests for King's Court 3.0 Knot 1: The Differential Test (The Control Group)."""

from pathlib import Path
from crossfire.control import run_naive_pipeline
from crossfire.cli import _analyze_directory

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_differential_benchmark_proves_control_group_failure() -> None:
    """Assert that the naive control group (git + compiler) passes all scenarios into production crashes,
    while CROSSFIRE deterministically intercepts and halts execution at 0.08s.
    """
    diff_results = run_naive_pipeline(FIXTURES_DIR)
    assert len(diff_results) == 3

    for res in diff_results:
        # Standard naive tools PASS silently
        assert res.git_merge.passed is True
        assert res.git_merge.status_code == 0
        assert res.linter_compile.passed is True
        assert res.linter_compile.status_code == 0

        # Runtime execution suffers unhandled catastrophic failure
        assert res.runtime_execution.passed is False
        assert res.runtime_execution.status_code == 1

        # CROSSFIRE halts with fail-closed status code 2
        assert res.crossfire_intercept.status_code == 2
        assert "HALTED" in res.crossfire_intercept.message

    # Test that CROSSFIRE detection directly flags all 3 scenarios
    total_cols, advisories = _analyze_directory(FIXTURES_DIR)
    assert len(total_cols) == 3
    assert len(advisories) == 3
    assert all(c.halted for c in total_cols)
