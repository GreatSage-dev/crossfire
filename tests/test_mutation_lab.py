"""Test suite verification for CROSSFIRE Mutation Testing Lab.

King's Court 3.0 // Universal Quality Signal (Anti-False-Positive Discipline).
Asserts that 100% of injected architectural mutations are caught and killed.
"""

from tests.mutation_lab import run_mutation_lab


def test_mutation_score_100_percent_killed() -> None:
    """Verify that all 8 deliberate architectural faults are caught (0 survivors)."""
    results, duration_ms = run_mutation_lab()

    assert len(results) == 8, f"Expected 8 mutants, got {len(results)}"

    survived = [r for r in results if not r.killed]
    assert len(survived) == 0, f"Mutants survived without detection: {[s.mutant_id for s in survived]}"

    killed_count = sum(1 for r in results if r.killed)
    assert killed_count == 8

    # Ensure mutation lab runs within microbenchmark latency budget (< 250 ms)
    assert duration_ms < 250.0, f"Mutation harness exceeded latency budget: {duration_ms:.2f} ms"
