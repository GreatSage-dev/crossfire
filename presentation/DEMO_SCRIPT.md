# CROSSFIRE — 3-Minute Video Demo Script
**Team Name:** Mrsage  
**Project:** CROSSFIRE — TCAS Collision Avoidance for Parallel AI Agents  
**Target Event:** IBM Bob 2.0 Hackathon  

---

### [0:00 - 0:30] THE HOOK (The Invisible Wound)
**Visual:** Open [`presentation/index.html`](index.html) or [`ui/index.html`](../ui/index.html) (Glass Cockpit with animated 3D Radar Globe).

> *"In 2026, development is multi-agent. With IBM Bob 2.0, teams spawn parallel subagents to work across multiple modules simultaneously. But Git was built in 2005 for lines of text. When Agent A refactors a model and Agent B writes an API route calling that model, Git reports 0 conflicts. Compilers and linters pass. The developer merges, and production crashes.*  
> *Traditional tools are blind to semantic collisions. That’s why we built **CROSSFIRE**."*

---

### [0:30 - 1:15] THE THREE FATAL COLLISIONS
**Visual:** Switch to Slide 3 in the presentation deck or the 3 Collision Cards in the web UI.

> *"Linters only check types and syntax. They cannot catch these three real-world disasters:*  
> *1. **Invariant Drift:** Agent A normalizes discount to float 0.0 to 1.0. Agent B passes integer 15 expecting 0 to 100. Both are numeric. Types match. Customer is charged 1500%.*  
> *2. **Lifecycle Desync:** Agent A makes token eviction asynchronous. Agent B assumes synchronous purge and deletes the user record. You now have a zombie authorization window.*  
> *3. **Contract Divergence:** Agent A changes missing items from raising an error to returning None. Agent B's try/except never triggers, permanently silencing restock logic."*

---

### [1:15 - 2:00] THE WORKING MACHINE (Bob IDE & PreToolUse Hook)
**Visual:** Show Bob IDE with the terminal and [`detector.py`](../crossfire/detector.py).

> *"CROSSFIRE is an Air Traffic Collision Avoidance System (TCAS) running directly inside IBM Bob 2.0's architecture.*  
> *As subagents draft code in their isolated scratchpads, our deterministic AST Invariant Miner extracts value bounds, lifecycles, and error contracts.*  
> *Our TCAS detector maps their invocation cones. If an intersection is detected, it triggers Bob's native **`PreToolUse` lifecycle hook with exit code 2**, physically halting the tool runner before corrupt code is ever written."*

---

### [2:00 - 2:40] THE LIVE DEMO & CLOSED-LOOP RESOLUTION
**Visual:** Show the terminal running `crossfire verify` or Bob IDE task where Subagent B is auto-steered.

> *"Watch this in action: when we run `crossfire verify`, our engine identifies the collisions in under 0.10 seconds and emits an imperative TCAS Resolution Advisory.*  
> *In Bob IDE, Bob acts as Subagent B, ingests the advisory, and automatically patches `agent_b_discount.py`—adding defensive normalization guards and aligning with Agent A.*  
> *When we re-verify, the `discount` collision is completely cleared.*  
> *Full closed-loop self-healing across parallel AI agents."*

---

### [2:40 - 3:00] THE CONCLUSION & BOBCOIN EFFICIENCY
**Visual:** Show `bob_sessions/` folder and the final slide.

> *"CROSSFIRE turns invisible multi-agent assumptions into an explicit, verifiable Assumption Ledger.*  
> *Best of all, because our AST radar runs deterministically offline in 80 milliseconds, we developed and verified this entire system burning just **1.08 Bobcoins** out of our 40-coin allocation—saving 80% of token burn by killing bad loops before they compile.*  
> *This is CROSSFIRE. Thank you."*
