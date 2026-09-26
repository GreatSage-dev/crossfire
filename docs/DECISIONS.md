# CROSSFIRE: Architectural Decision Records (ADR)

### Standard: King's Court 3.0 / System Primitives

---

### ADR-001: Pure AST Static Extraction vs. LLM Self-Reflection
* **Context:** Determining how to extract invariant assumptions from subagent scratchpads.
* **Option A (Rejected):** Prompting an LLM to "review Agent A and Agent B's code and report conflicts."
  * *Why Rejected:* Non-deterministic, introduces 2–6s API latency, costs tokens on every file write, and suffers from hallucinated false positives.
* **Option B (Accepted):** Python native `ast.NodeVisitor` inspecting assertion bounds, type defaults, and exception nodes.
  * *Rationale:* Runs in $< 2\text{ms}$, 100% deterministic, zero network calls, zero token burn.

---

### ADR-002: Epistemic Refusal via the Tri-State Law (Knot 3)
* **Context:** Multi-agent claim extraction often encounters ambiguous, un-typed, or dynamically reflected parameters.
* **Decision:** Replace binary `halted: bool` with `TCASStatus`:
  1. `CLEAR`: High confidence ($\ge 0.70$) matching invariants.
  2. `COLLISION_HALT`: High confidence ($\ge 0.70$) conflicting invariants.
  3. `UNKNOWN_SUSPEND`: Confidence $< 0.70$ or ambiguous dynamic behavior.
* **Rationale:** When evidence cannot confirm contract agreement, guessing "valid" introduces silent bugs, while guessing "collision" introduces false positive noise. `UNKNOWN_SUSPEND` halts execution fail-closed for human or supervisor review.

---

### ADR-003: Non-Blocking Subshell Stdin Handling in PreToolUse Hook
* **Context:** In PowerShell, CI, and nested automation subshells, `sys.stdin.isatty()` evaluates to `False` even when no data is being piped into stdin.
* **Vulnerability Identified:** An initial implementation called `sys.stdin.read()` whenever `not sys.stdin.isatty()`, causing the CLI to hang indefinitely waiting for EOF when executed with directory arguments.
* **Decision:** Prioritize explicit CLI arguments (`cli_args`) over stdin reading. Only attempt `stdin.read()` if no payload was passed AND no CLI arguments were supplied.

---

### ADR-004: In-Memory Bytecode Compilation for Differential Testing
* **Context:** Executing the Differential Benchmark (`control.py`) on Windows platforms.
* **Vulnerability Identified:** Using `tempfile.NamedTemporaryFile` with `py_compile.compile` caused `[WinError 5] Access is denied` due to concurrent atomic file locking on Windows.
* **Decision:** Use Python built-in in-memory `builtins.compile(source, filename, "exec")` which verifies complete syntax and bytecode emission without filesystem handle collisions.
