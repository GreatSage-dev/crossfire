# RFC-0042: Standardizing Semantic Conflict Interceptions in IBM Bob 2.0 PreToolUse Hook

**RFC Number:** RFC-0042  
**Title:** Standardized PreToolUse Semantic Conflict Interception Protocol (`Exit Code 2`)  
**Author:** Promise Philip ([@GreatSage-dev](https://github.com/GreatSage-dev)), Team Mrsage  
**Status:** Proposed / Upstream RFC  
**Target:** IBM Bob 2.0 Harness & Multi-Agent Orchestrator  
**Date:** September 2026  

---

## 1. Abstract

In IBM Bob 2.0's multi-agent architecture, specialized subagents execute tasks concurrently in isolated scratchpads. While file-isolated execution prevents raw write-lock collisions, it creates an invisible failure mode: **inter-scratchpad semantic conflict**. Subagents write conforming local syntax while introducing conflicting assumptions about numerical domains, coroutine execution lifecycles, and exception contracts.

This RFC proposes standardizing **Exit Code 2** (`SEMANTIC_CONFLICT_INTERCEPT`) within the `PreToolUse` hook specification. When a hook returns Exit Code 2, Bob's harness suspends tool execution fail-closed, ingests a standardized `ResolutionAdvisory` from `stderr`, and steers the offending subagent with an imperative remediation prompt before resuming tool execution.

---

## 2. Motivation & Problem Statement

Currently, IBM Bob 2.0 lifecycle hooks support binary evaluation:
- `Exit Code 0`: Hook passes; tool execution proceeds immediately.
- `Exit Code 1`: Generic hook failure; triggers an unhandled execution error or blind retry.

When two subagents generate diverging domain contracts:
1. **Subagent A** writes `def calculate(price, discount=0.15): assert 0.0 <= discount <= 1.0`.
2. **Subagent B** writes `calculate(price, discount=15)`.

Standard git merge-tree inspection detects **0 merge conflicts** (separate files). Compilers detect **0 syntax errors**. If Bob proceeds to run `PreToolUse` with binary exit codes, either:
- The conflict passes silently into runtime crashes, or
- A generic `Exit Code 1` causes Bob to regenerate code without understanding *why* the contract failed.

---

## 3. Specification: The Tri-State Hook Protocol

We propose extending Bob's harness hook runner with a tri-state exit code contract:

| Exit Code | Status Code | Harness Action |
| :--- | :--- | :--- |
| **`0`** | `CLEAR` | Unconditional approval. Tool executes. |
| **`1`** | `RUNTIME_ERROR` | Fatal hook infrastructure failure. Aborts session. |
| **`2`** | `SEMANTIC_CONFLICT` | Intercepted invariant drift. Harness reads `ResolutionAdvisory` from `stderr` and dispatches auto-remediation to the target subagent. |

### Stderr Payload Schema (`application/x-tcas-advisory+json`):
```json
{
  "collision_class": "invariant_drift",
  "symbol": "discount",
  "severity": 0.95,
  "target_agent": "subagent_b",
  "recommended_action": "Normalize discount to float domain [0.0, 1.0]",
  "patch_hint": "discount = float(discount) / 100.0 if discount > 1.0 else float(discount)"
}
```

---

## 4. Reference Implementation Patch

The complete git patch for IBM Bob 2.0 harness hook dispatchers is preserved in [`docs/upstream/bob_semantic_conflict.patch`](bob_semantic_conflict.patch).

---

## 5. Security & Fail-Closed Epistemic Refusal

In accordance with safety principles, if the semantic analysis hook encounters low confidence ($< 0.70$) due to dynamic reflection or unresolvable imports, it enters `UNKNOWN_SUSPEND` and emits Exit Code 2 with an epistemic warning rather than guessing contracts.
