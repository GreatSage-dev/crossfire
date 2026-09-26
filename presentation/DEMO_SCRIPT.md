# CROSSFIRE — The Winning 3-Minute Demo Video Script

**Project:** CROSSFIRE — Collision Avoidance for Parallel AI Agents in IBM Bob 2.0  
**Team:** Mrsage (LabLab: Mrsage | GitHub: GreatSage-dev)  
**Target Duration:** Exactly 3:00 (180 seconds)  
**Presenter Delivery Note:** Speak in a calm, confident, senior engineering tone. Zero marketing fluff. Zero breathless hype. Every claim is backed by what is on screen.

---

## Shot-by-Shot Video Blueprint

```
[0:00 - 0:30] ACT 1: THE INVISIBLE WOUND (The Hook & Emotional Weight)
[0:30 - 1:15] ACT 2: THE FOUR ARCHETYPES & THE DIFFERENTIAL MATRIX
[1:15 - 1:55] ACT 3: THE ENGINE (AST Mining, Tri-State Law & Bob PreToolUse)
[1:55 - 2:35] ACT 4: THE LIVE PROOF (Interactive Sandbox & Mutation Lab)
[2:35 - 3:00] ACT 5: THE CORE THESIS & UPSTREAM RFC (The Closing Punchline)
```

---

### ACT 1: THE INVISIBLE WOUND (0:00 – 0:30)

#### VISUAL (0:00 – 0:15)
Split-screen video or fast cut:
- **Left:** Terminal showing a multi-agent Git merge: `Auto-merging... 0 conflicts`. Next command: `mypy .` -> `Success: no issues found in 2 source files`.
- **Right:** A simulated production order log or gateway log suddenly flashing red: `AssertionError: timeout 5000 exceeds max 60s` / `CATASTROPHIC: Customer charged -1400% on order`.

#### NARRATION (Voiceover, calm, measured):
> *"Here is the most dangerous moment in autonomous software engineering:*  
> *Two AI agents finish their work in parallel. Git reports zero merge conflicts. Mypy and your linter report zero type errors. Everything looks green.*  
> *Then your system deploys, and an order is charged negative fourteen hundred dollars.*  
> *Why? Because Git was built twenty years ago to compare lines of text. Linters only check syntax. Neither tool knows what your agents were actually assuming."*

#### VISUAL (0:15 – 0:30)
Camera transitions to the CROSSFIRE web console ([`https://crossfire-production.vercel.app`](https://crossfire-production.vercel.app/)) showing the dark radar sweep and Assumption Ledger with the status badge: `3 COLLISION(S) DETECTED — AGENT EXECUTION HALTED`.

#### NARRATION:
> *"This is CROSSFIRE. It is an Air Traffic Collision Avoidance System designed for the era of parallel AI subagents in IBM Bob 2.0. It intercepts incompatible assumptions across isolated agent scratchpads before those assumptions become a system."*

---

### ACT 2: THE FOUR ARCHETYPES & THE DIFFERENTIAL (0:30 – 1:15)

#### VISUAL (0:30 – 0:50)
Screen shows the code comparison for **Timeout Unit Drift** ([`tests/fixtures/agent_a_timeout.py`](../tests/fixtures/agent_a_timeout.py) vs [`agent_b_timeout.py`](../tests/fixtures/agent_b_timeout.py)):
- Subagent A: `timeout: int = 30`, `assert 1 <= timeout <= 60` (expects seconds).
- Subagent B: `timeout: int = 5000` (expects milliseconds).

#### NARRATION:
> *"Consider the hardest problem in static analysis: same-type semantic unit drift.*  
> *Here, Subagent A configures an API gateway with `timeout` as an integer between one and sixty seconds.*  
> *In another file, Subagent B calls that gateway passing integer five thousand, assuming milliseconds.*  
> *Both values are valid integers. Mypy sees `int == int` and passes cleanly. But at runtime, passing five thousand causes a catastrophic gateway failure.*  
> *CROSSFIRE's AST miner doesn't just check the type annotation. It extracts the boundary contract: `int[1, 60]` versus literal `int[5000]`. It flags the collision before a single byte touches disk."*

#### VISUAL (0:50 – 1:15)
Screen pans across the **Differential Matrix** on the landing page or terminal (`python run_receipt.py`):
```text
Collision Archetype          | Git Merge   | Linter / Mypy | Standard Exec   | CROSSFIRE TCAS
-----------------------------------------------------------------------------------------
1. Invariant Drift (scale)   | 0 conflicts | 0 type errors | -$1,400 CHARGE  | HALTED (EXIT 2)
2. Lifecycle Desync (async)  | 0 conflicts | 0 type errors | EVENT LOOP DEAD | HALTED (EXIT 2)
3. Contract Divergence (err) | 0 conflicts | 0 type errors | SILENT CORRUPT  | HALTED (EXIT 2)
4. Unit Drift (int vs int)   | 0 conflicts | mypy: 0 err   | GATEWAY TIMEOUT | HALTED (EXIT 2)
```

#### NARRATION:
> *"In our four controlled collision cases, Git and static type checking do not detect the cross-agent semantic conflict.*  
> *CROSSFIRE intercepts and halts the tool runner across all four."*

---

### ACT 3: THE ENGINE & IBM BOB 2.0 (1:15 – 1:55)

#### VISUAL (1:15 – 1:35)
Show the architecture diagram and Bob 2.0 IDE configuration:
- Highlight [`crossfire/hook.py`](../crossfire/hook.py) and the `PreToolUse` lifecycle hook protocol.
- Show diagram of the **Tri-State Law** (`COLLISION_HALT`, `UNKNOWN_SUSPEND`, `CLEAR`).

#### NARRATION:
> *"How does it work?*  
> *CROSSFIRE integrates directly into IBM Bob 2.0 via its native `PreToolUse` lifecycle hook.*  
> *Whenever a subagent attempts a tool write, CROSSFIRE mines the active scratchpads using generalized AST visitors—extracting domain invariants, temporal lifecycles, and exception returns.*  
> *Then it applies the Tri-State Law. Binary pass/fail is dangerous in agent swarms. If confidence is high and assumptions diverge, CROSSFIRE halts execution with Bob's exit code 2 and returns an imperative resolution advisory.*  
> *If an assumption is ambiguous or dynamic, CROSSFIRE enters `UNKNOWN_SUSPEND`—it refuses to hallucinate a guess, fail-closing safely for human review."*

#### VISUAL (1:35 – 1:55)
Show Bob IDE terminal:
- Hook fires.
- Exit code 2 stops the agent write.
- Resolution advisory appears in stderr: `[TCAS ADVISORY] Target: Subagent B | Action: Convert millisecond timeout to seconds: timeout = timeout // 1000`.

#### NARRATION:
> *"Because Bob respects exit code 2, the offending write is physically blocked. Subagent B ingests the advisory, patches its assumption, and re-executes. The loop heals itself before merging."*

---

### ACT 4: THE LIVE PROOF (1:55 – 2:35)

#### VISUAL (1:55 – 2:15)
Switch to the **Live Conflict Sandbox** on the deployed dashboard ([`https://crossfire-production.vercel.app/dashboard`](https://crossfire-production.vercel.app/dashboard)):
- Presenter types arbitrary custom code into Subagent A and Subagent B live on camera (e.g. `assert 0.0 <= fee_ratio <= 0.05` vs `fee_ratio = 5`).
- Clicks `[▶ Analyze Live Conflict]`.
- Watch the Assumption Ledger populate, threat dots plot onto the radar sweep, and the advisory card render instantly.

#### NARRATION:
> *"This isn't hardcoded mock data. In our live deployed operations dashboard, any judge can open the Conflict Sandbox, enter arbitrary Python code with unseen symbols, and watch CROSSFIRE extract invariants and resolve conflicts live in real time."*

#### VISUAL (2:15 – 2:35)
Switch to terminal and run:
`python tests/mutation_lab.py` or `python run_receipt.py`.
Camera focuses on terminal:
```text
Architectural Mutants: 8 / 8 Killed (100.0%)
Mutation Lab Latency:  23.36 ms
  * [KILLED] MUTANT-01: Bypass Value Domain Drift    -> crossfire.detector
  * [KILLED] MUTANT-02: Bypass Lifecycle Desync      -> crossfire.detector
  * [KILLED] MUTANT-04: Epistemic Refusal Bypass     -> crossfire.detector
  * [KILLED] MUTANT-05: Hook Fail-Open Inversion     -> crossfire.hook
Attestation: 8/8 injected architectural faults killed (suite proves non-tautological)
```

#### NARRATION:
> *"To prove our test suite is not a tautology, we built a Mutation Testing Lab. We injected eight deliberate architectural mutations into our detector, hook, and epistemic logic.*  
> *Our test suite killed all eight mutants in twenty-three milliseconds. When the logic breaks, the suite goes red immediately."*

---

### ACT 5: THE CORE THESIS & UPSTREAM RFC (2:35 – 3:00)

#### VISUAL (2:35 – 2:50)
Show the repository root on GitHub:
- [`docs/upstream/RFC_BOB_PRETOOLUSE_SEMANTIC_CONFLICT.md`](../docs/upstream/RFC_BOB_PRETOOLUSE_SEMANTIC_CONFLICT.md)
- [`bob_sessions/`](../bob_sessions/) verification logs showing 1.08 Bobcoins used.

#### NARRATION:
> *"We didn't just build an isolated tool—we submitted an upstream RFC and patch to IBM Bob proposing a standard semantic conflict protocol for multi-agent scratchpads.*  
> *And by catching incompatible loops early, we built and verified this entire system burning just one point zero eight Bobcoins out of our forty-coin allocation."*

#### VISUAL (2:50 – 3:00)
Return to the hero graphic with the Core Thesis highlighted:
> **"Git detects textual conflicts.**  
> **Tests detect behavioral failures in isolation.**  
> **CROSSFIRE detects conflicts between the assumptions of autonomous software agents before those assumptions become a system."**

#### NARRATION:
> *"Git detects textual conflicts. Tests detect behavioral failures in isolation.*  
> *CROSSFIRE detects conflicts between the assumptions of autonomous software agents before those assumptions become a system.*  
> *Try it live at crossfire-production.vercel.app. We are Team Mrsage. Thank you."*

---

## Presenter Recording Checklist

| Item | What to prepare before hitting record |
| :--- | :--- |
| **Tab 1: Live Webpage** | [`https://crossfire-production.vercel.app`](https://crossfire-production.vercel.app/) and [`/dashboard`](https://crossfire-production.vercel.app/dashboard) opened, zoomed to 110% for crystal-clear readability. |
| **Tab 2: VS Code / Bob IDE** | Terminal open at repo root, clear screen (`cls`), ready to run `python run_receipt.py`. |
| **Tab 3: Upstream RFC** | [`docs/upstream/RFC_BOB_PRETOOLUSE_SEMANTIC_CONFLICT.md`](../docs/upstream/RFC_BOB_PRETOOLUSE_SEMANTIC_CONFLICT.md) rendered on GitHub. |
| **Audio** | Clear microphone, quiet room, steady deliberate pacing. Do not rush. |
| **Video Resolution** | 1080p 60fps or 4K 30fps. Full screen capture. |
