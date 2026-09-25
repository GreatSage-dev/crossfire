"""IBM Bob 2.0 PreToolUse hook implementation for intercepting agent collisions."""

import json
from pathlib import Path
import sys
from typing import Any, Optional

from crossfire.detector import detect_collisions
from crossfire.miner import extract_claims
from crossfire.models import CollisionVector, InvariantClaim
from crossfire.resolver import generate_advisory


def format_advisory_stderr(advisory) -> str:
    """Format a ResolutionAdvisory into an imperative aviation-style TCAS alert."""
    vec: CollisionVector = advisory.vector
    lines = [
        "",
        "=" * 80,
        "[CROSSFIRE TCAS INTERCEPT] IBM BOB 2.0 PRETOOLUSE HOOK HALTED (CODE 2)",
        "=" * 80,
        f"CRITICAL COLLISION: {vec.collision_class.upper()} (Severity: {vec.severity:.2f})",
        f"Symbol:           {vec.claim_a.symbol}",
        f"Description:      {vec.description}",
        "-" * 80,
        "RESOLUTION ADVISORY (TCAS STEERING):",
        f"Target Agent:     {advisory.target_agent}",
        f"Action:           {advisory.recommended_action}",
        "Patch Hint:",
        f"{advisory.patch_hint}",
        "=" * 80,
        "",
    ]
    return "\n".join(lines)


def load_scratchpads(payload: dict[str, Any], extra_args: list[str]) -> dict[str, str]:
    """Extract agent_id -> source_code mapping from payload or CLI arguments."""
    scratchpads: dict[str, str] = {}

    # Case 1: Payload contains 'agents' dict {agent_id: source_or_path}
    if "agents" in payload and isinstance(payload["agents"], dict):
        for agent_id, content in payload["agents"].items():
            path = Path(str(content))
            if path.is_file():
                scratchpads[agent_id] = path.read_text(encoding="utf-8")
            else:
                scratchpads[agent_id] = str(content)

    # Case 2: Payload contains 'scratchpads' or 'files' list
    file_list = payload.get("scratchpads") or payload.get("files") or payload.get("paths")
    if file_list and isinstance(file_list, list):
        for item in file_list:
            if isinstance(item, dict):
                agent_id = item.get("agent_id") or Path(item.get("path", "agent")).stem
                path = Path(item["path"])
                if path.is_file():
                    scratchpads[agent_id] = path.read_text(encoding="utf-8")
            elif isinstance(item, str):
                path = Path(item)
                if path.is_file():
                    agent_id = path.stem
                    scratchpads[agent_id] = path.read_text(encoding="utf-8")

    # Case 3: Payload contains 'tool_input' dictionary
    if "tool_input" in payload and isinstance(payload["tool_input"], dict):
        t_input = payload["tool_input"]
        sub_files = t_input.get("files") or t_input.get("scratchpads")
        if isinstance(sub_files, list):
            for f in sub_files:
                p = Path(f)
                if p.is_file():
                    scratchpads[p.stem] = p.read_text(encoding="utf-8")

    # Case 4: Extra CLI arguments passed as files or directories
    for arg in extra_args:
        path = Path(arg)
        if path.is_file() and path.suffix == ".py":
            scratchpads[path.stem] = path.read_text(encoding="utf-8")
        elif path.is_dir():
            for py_file in sorted(path.glob("*.py")):
                if py_file.name != "__init__.py":
                    scratchpads[py_file.stem] = py_file.read_text(encoding="utf-8")

    return scratchpads


def run_hook(
    payload: Optional[dict[str, Any] | str] = None,
    args: Optional[list[str]] = None,
    exit_on_result: bool = False,
) -> int:
    """Execute the IBM Bob 2.0 PreToolUse hook.

    Args:
        payload: Optional parsed JSON payload or JSON string.
        args: Optional list of command-line arguments.
        exit_on_result: Whether to call sys.exit() or return exit code.

    Returns:
        0 if verification clean, 2 if collision halted execution.
    """
    raw_payload: dict[str, Any] = {}
    cli_args = list(args if args is not None else sys.argv[1:])

    # Parse payload if provided
    if isinstance(payload, dict):
        raw_payload = payload
    elif isinstance(payload, str) and payload.strip():
        try:
            raw_payload = json.loads(payload)
        except json.JSONDecodeError:
            pass

    # Read stdin if payload not explicitly provided
    if not raw_payload and not sys.stdin.isatty():
        try:
            stdin_content = sys.stdin.read().strip()
            if stdin_content:
                raw_payload = json.loads(stdin_content)
        except Exception:
            pass

    scratchpads = load_scratchpads(raw_payload, cli_args)

    if len(scratchpads) < 2:
        # Fewer than 2 scratchpads means no cross-agent collision is possible
        if exit_on_result:
            sys.exit(0)
        return 0

    # Mine invariant claims for each scratchpad
    claims_by_agent: dict[str, list[InvariantClaim]] = {}
    for agent_id, source in scratchpads.items():
        claims_by_agent[agent_id] = extract_claims(source, agent_id=agent_id)

    # Detect collisions across agent pairs
    agent_names = list(claims_by_agent.keys())
    all_collisions: list[CollisionVector] = []
    for i in range(len(agent_names)):
        for j in range(i + 1, len(agent_names)):
            a_id, b_id = agent_names[i], agent_names[j]
            collisions = detect_collisions(claims_by_agent[a_id], claims_by_agent[b_id])
            all_collisions.extend(collisions)

    # Check for halted collisions
    halted_collisions = [c for c in all_collisions if c.halted]

    if halted_collisions:
        for collision in halted_collisions:
            advisory = generate_advisory(collision)
            sys.stderr.write(format_advisory_stderr(advisory))
        if exit_on_result:
            sys.exit(2)
        return 2

    if exit_on_result:
        sys.exit(0)
    return 0


def main() -> None:
    """CLI entrypoint for PreToolUse hook."""
    run_hook(exit_on_result=True)


if __name__ == "__main__":
    main()
