# CROSSFIRE: Air Traffic Collision Avoidance System (TCAS) for Parallel AI Agents

[![Live Web Demo](https://img.shields.io/badge/Live%20Demo-crossfire--production.vercel.app-E8611A?style=flat-square&logo=vercel)](https://crossfire-production.vercel.app/)
[![Deterministic Tests](https://img.shields.io/badge/pytest-19%20passed%20%5B0.48s%5D-brightgreen?style=flat-square)](tests/)
[![Mutation Score](https://img.shields.io/badge/Mutation%20Score-8%2F8%20Killed%20%5B100%25%5D-brightgreen?style=flat-square)](tests/mutation_lab.py)
[![Bob IDE Verified](https://img.shields.io/badge/IBM%20Bob%202.0-Verified%20Session-0062FF?style=flat-square)](bob_sessions/)
[![Exit Code Protocol](https://img.shields.io/badge/PreToolUse-Exit%20Code%202%20Halt-E8611A?style=flat-square)](crossfire/hook.py)
[![Zero-Dependency Receipt](https://img.shields.io/badge/run__receipt.py-Deterministic%20Proof-brightgreen?style=flat-square)](run_receipt.py)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](LICENSE)

$$\text{\textbf{INTERCEPT}} \longrightarrow \text{\textbf{MINE (AST)}} \longrightarrow \text{\textbf{COLLIDE (TCAS)}} \longrightarrow \text{\textbf{HALT (EXIT 2)}} \longrightarrow \text{\textbf{AUTO-STEER}}$$

> **The Core Thesis:**  
> *"Git detects textual conflicts. Tests detect behavioral failures in isolation. CROSSFIRE detects conflicts between the assumptions of autonomous software agents before those assumptions become a system."*

When IBM Bob 2.0 spawns parallel subagents in isolated scratchpads, each agent works in isolation. Agent A updates an architectural invariant; Agent B calls that code in another file with an incompatible assumption. Git reports 0 textual conflicts. Linters, compilers, and strict type checkers (`mypy`) report 0 type errors. Production crashes. CROSSFIRE makes invisible cross-agent assumptions visible and coordinated before code is written.

---

## The Dual Ingress Doors (For Judges)

### Ingress Path A: The Glass Cockpit (Live Deployed Web Console)
* 🌐 **Live Web Demo:** [https://crossfire-production.vercel.app](https://crossfire-production.vercel.app/)
* 🛰️ **Live Operations Console:** [https://crossfire-production.vercel.app/dashboard](https://crossfire-production.vercel.app/dashboard)
* **Landing Interface ([`index.html`](index.html)):** Command aesthetic with warm atmospheric depth (`#0D0D0D`, `#161616`, `#E8611A`, `#F5A623`), Lenis smooth scrolling, staggered GSAP card entrances, and clean radar telemetry.
* **Operations Dashboard ([`dashboard.html`](dashboard.html)):** Bento grid with KPI metric cards, active agent telemetry badges, live Assumption Ledger, terminal event stream, real-time TCAS sweep radar, and an **Interactive Conflict Sandbox** where judges can type arbitrary Python code to watch live AST extraction and collision resolution.
* **Interactive Live Stream:** Connects live to `crossfire live` over WebSocket (`ws://127.0.0.1:8765`), updating radar sweeps and threat vectors on file modification, with automatic offline simulation fallback.

### Ingress Path B: The Sub-Second Terminal Verification (Zero Dependencies)
Run the zero-external-dependency mathematical verification harness:
```bash
python run_receipt.py
```
**Terminal Output:**
```text
==============================================================================
 CROSSFIRE // DETERMINISTIC TCAS VERIFICATION & DIFFERENTIAL RECEIPT
 Standard: King's Court 3.0 (Knot 1: Differential Test | Knot 3: Tri-State)
==============================================================================

[SECTION 1: THE DIFFERENTIAL BENCHMARK // CONTROL GROUP VS CROSSFIRE]
Collision Archetype          | Git Merge   | Linter/Types  | Standard Exec   | CROSSFIRE TCAS
--------------------------------------------------------------------------------
1. Invariant Drift (scale)   | 0 conflicts | 0 type errors | CATASTROPHIC*   | HALTED (EXIT 2)
2. Lifecycle Desync (async)  | 0 conflicts | 0 type errors | RUNTIME CRASH   | HALTED (EXIT 2)
3. Contract Divergence (err) | 0 conflicts | 0 type errors | SILENT FAIL     | HALTED (EXIT 2)
4. Unit Drift (int vs int)   | 0 conflicts | mypy 0 errors | GATEWAY TIMEOUT | HALTED (EXIT 2)

* Differential proof: Git, linters, and mypy pass 100% cleanly across all 4 scenarios.
  Standard tools cannot see inter-scratchpad domain assumptions. CROSSFIRE intercepts all 4.

[SECTION 2: TRI-STATE EPISTEMIC SAFETY AUDIT]
  * Deterministic Divergences (Conf >= 0.85): 4 / 4 -> State: COLLISION_HALT (Exit 2)
  * Ambiguous Bounds (Conf < 0.70):           Tested -> State: UNKNOWN_SUSPEND (Refuses to guess)
  * Aligned Contracts (Domains Match):        Tested -> State: CLEAR (Resume execution)

[SECTION 3: MUTATION TESTING HARNESS // ANTI-TAUTOLOGY PROOF]
  Architectural Mutants: 8 / 8 Killed (100.0%)
  Attestation:           8/8 injected architectural faults killed (suite proves non-tautological)

[SECTION 4: AUDIT RECEIPT]
  Receipt Fingerprint:   sha256:8d2d331051d5eaef
  AST Mining Latency:    ~3.9 ms
  Mutation Score:        8/8 Killed (100.0%)
  Total Execution Time:  ~35 ms
  Deterministic Check:   100% PASS (Zero network calls, zero LLM variance)
==============================================================================
```

---

## Architectural Enforcement Matrix (King's Court 3.0 Standard)

| Layer | Invariant Mechanism | Enforcement Point | Fail-Closed Policy |
| :--- | :--- | :--- | :--- |
| **AST Mining** | Generalized boundary assertions (`[0.0, 1.0]` vs `[0, 100]` or `[1, 60]`) | [`crossfire/miner.py`](crossfire/miner.py) | Confidence weighted (0.85–1.0) |
| **AST Mining** | Async coroutine vs synchronous blocking function detection | [`crossfire/miner.py`](crossfire/miner.py) | Explicit lifecycle mapping |
| **AST Mining** | Return `None` vs explicit `raise Exception` contract matching | [`crossfire/miner.py`](crossfire/miner.py) | Exception symbol extraction |
| **Detection** | Tri-State epistemic classification (`CLEAR` vs `COLLISION_HALT` vs `UNKNOWN_SUSPEND`) | [`crossfire/detector.py`](crossfire/detector.py) | Confidence < 0.70 enters `UNKNOWN_SUSPEND` |
| **Hook Protocol** | Bob 2.0 PreToolUse hook execution intercept | [`crossfire/hook.py`](crossfire/hook.py) | Non-zero exit code (`sys.exit(2)`) |
| **Resolution** | TCAS imperative patch advisory generation | [`crossfire/resolver.py`](crossfire/resolver.py) | Imperative steering in `stderr` |
| **Telemetry** | Live WebSocket broadcast engine (`ws://127.0.0.1:8765`) | [`crossfire/broadcaster.py`](crossfire/broadcaster.py) | Async fan-out with offline fallback |

---

## Why Traditional Tools Are Blind (The 4 Archetypes)

Linters, compilers, and git line merges only check syntax and type signatures. Even strict type checkers like `mypy` and `pyright` fail when types match but semantics drift:

| Collision Archetype | What Compiler / Linter / Mypy Sees | What Actually Happens (The Crash) | How CROSSFIRE Intercepts |
| :--- | :--- | :--- | :--- |
| **1. Invariant / Value Domain Drift** | Both variables are typed `float` or numeric. Valid syntax. | Agent A normalized discount to `[0.0..1.0]`. Agent B passes `15` expecting `[0..100]`. **Customer charged 1500%**. | AST miner extracts boundary assertions (`assert 0.0 <= discount <= 1.0` vs `0 <= discount <= 100`). Flags `INVARIANT_DRIFT` (0.95). |
| **2. State & Temporal Lifecycle Desync** | Function signatures match. Both return `bool`. | Agent A made token invalidation async. Agent B assumes synchronous purge and deletes DB record. **Zombie auth security hole**. | AST miner detects `async def` coroutine vs synchronous function definition. Flags `LIFECYCLE_DESYNC` (0.85). |
| **3. Contract & Exception Divergence** | Both return valid Python objects. | Agent A changes missing item from `raise ItemNotFoundError` to `return None`. Agent B's `try/except` never triggers. **Restock logic dead**. | AST miner inspects return statements vs explicit `raise` nodes. Flags `CONTRACT_DIVERGENCE` (0.90). |
| **4. Same-Type Semantic Unit Drift** | Both variables are typed `int`. **`mypy` passes with 0 errors**. | Agent A specifies timeout in seconds (`assert 1 <= timeout <= 60`). Agent B passes `5000` (milliseconds). **Gateway timeout / connection rejected**. | AST miner extracts domain bounds (`int[1, 60]`) vs assigned literal (`int[val=5000]`). Flags `INVARIANT_DRIFT` (0.95) before tool writes file. |

---

## The Post-Build Evidence & Decision Corpus

* [`evidence/EVAL_REPORT.md`](evidence/EVAL_REPORT.md) — The complete evaluation benchmark, Knot 1 differential control analysis, microsecond latency breakdown, and disarming tuning disclosures.
* [`docs/SPONSOR_ABLATION.md`](docs/SPONSOR_ABLATION.md) — 4-point ablation matrix proving IBM Bob 2.0's `PreToolUse` hook and isolated scratchpads are strictly load-bearing.
* [`docs/DECISIONS.md`](docs/DECISIONS.md) — Architectural Decision Records (ADRs) documenting Tri-State epistemic laws and patched edge cases.

---

## Evidence of IBM Bob Usage (`bob_sessions/`)

In compliance with the official IBM Bob 2.0 Hackathon requirements, all Bob IDE session consumption summaries are preserved in [`bob_sessions/`](bob_sessions/):

* `mrsage_task01_ast_miner_summary.png` — Architectural indexation & AST extraction mapping
* `mrsage_task02_collision_detector_summary.png` — Terminal verification & exit code 2 hook validation
* `mrsage_task03_resolution_advisory_summary.png` — Subagent B closed-loop auto-steering & diff application
* `mrsage_task04_verification_cleared_summary.png` — Verification of cleared collision & residual radar state

*Total Bobcoin Consumption across full build:* **1.08 Bobcoins** (out of 40 allocated).

---

## The Radical Honesty Table

| Component | Status | Implementation Details |
| :--- | :--- | :--- |
| **AST Invariant Extraction** | **Production-Grade** | Pure Python `ast.NodeVisitor` inspecting asserts, parameters, and expressions. Zero external network calls. |
| **Collision Detection Engine** | **Production-Grade** | Graph intersection of symbol mutation cones vs invocation cones across 3 collision classes. |
| **Tri-State Epistemic Classification** | **Production-Grade** | First-class `UNKNOWN_SUSPEND` state that refuses to guess on low-confidence contracts (< 0.70). |
| **PreToolUse Hook Contract** | **Production-Grade** | Complies with Bob 2.0's fail-closed specification (exit code 2 halts runner). |
| **Closed-Loop Resolution Patching** | **Production-Grade** | Imperative patch generation with AST boundary normalization. |
| **Glass Cockpit UI** | **Production-Grade** | Growaz-inspired landing page, uncongested bento dashboard, SVG TCAS radar, and live WebSocket telemetry. |
| **Dynamic Runtime Reflection** | **Out of Scope** | Dynamic runtime string evaluation (`getattr(mod, f"dyn_{name}")`) is intentionally excluded from static AST analysis. |

---

## Mutation Testing Lab (Anti-False-Positive Discipline)

> *"In any project, you can prove your test suite isn't a false positive by deliberately breaking code and showing the tests catch it."*

To eliminate the risk of tautological tests, CROSSFIRE includes an in-memory **Mutation Testing Lab** ([`tests/mutation_lab.py`](tests/mutation_lab.py)) that deliberately injects 8 architectural faults:

| Mutant ID | Injected Fault | Target Subsystem | Status |
| :--- | :--- | :--- | :--- |
| **MUTANT-01** | Bypass value domain drift detection | `crossfire.detector.detect_collisions` | 🛑 **KILLED** |
| **MUTANT-02** | Bypass lifecycle desync detection | `crossfire.detector.detect_collisions` | 🛑 **KILLED** |
| **MUTANT-03** | Bypass error contract divergence detection | `crossfire.detector.detect_collisions` | 🛑 **KILLED** |
| **MUTANT-04** | Bypass epistemic refusal (guess on confidence < 0.70) | `crossfire.detector._evaluate_tri_state` | 🛑 **KILLED** |
| **MUTANT-05** | Hook fail-open inversion (return code 0 instead of 2) | `crossfire.hook.run_hook` | 🛑 **KILLED** |
| **MUTANT-06** | Suppress collision severity score to 0.0 | `crossfire.detector.detect_collisions` | 🛑 **KILLED** |
| **MUTANT-07** | AST bounds corruption (treat int 100 as float) | `crossfire.miner._ValueDomainVisitor` | 🛑 **KILLED** |
| **MUTANT-08** | Wipe TCAS Resolution Advisory patch hint | `crossfire.resolver.generate_advisory` | 🛑 **KILLED** |

**Mutation Score:** **8 / 8 Mutants Killed (100.0%)** in 12.75 ms.  
Every architectural deviation in detection, scoring, or fail-closed gating turns the test suite red immediately.

---

## Installation & Test Suite

```bash
# Clone the repository
git clone https://github.com/GreatSage-dev/crossfire.git
cd crossfire

# Install dependencies (or pip install -r requirements.txt)
pip install -e .

# Run zero-dependency mathematical receipt & mutation audit (< 0.02s)
python run_receipt.py

# Run standalone architectural mutation testing lab (8/8 killed in 14ms)
python tests/mutation_lab.py

# Run full test suite (17 tests in 0.42s)
pytest -v

# Run deterministic TCAS verifier (exits with code 2)
crossfire verify

# Start live real-time WebSocket telemetry stream for the dashboard
crossfire live
```

---

## Team Mrsage
Built for the **IBM Bob 2.0 Hackathon** (Sept 25–27, 2026).  
Team on LabLab: **Mrsage** | GitHub: **GreatSage-dev**
