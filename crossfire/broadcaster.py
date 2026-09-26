"""WebSocket broadcaster streaming CROSSFIRE telemetry and radar states to the UI console."""

from __future__ import annotations
import asyncio
import json
import logging
from pathlib import Path
import time
from typing import Any, Set
import websockets

from crossfire.detector import detect_collisions
from crossfire.miner import extract_claims
from crossfire.resolver import generate_advisory

logger = logging.getLogger("crossfire.broadcaster")


def _compute_telemetry_payload(path: Path) -> dict[str, Any]:
    """Mine claims and compute active collision vectors for the live telemetry stream."""
    files = sorted(path.glob("*.py"))
    agent_a_files = [f for f in files if "agent_a" in f.name.lower()]
    agent_b_files = [f for f in files if "agent_b" in f.name.lower()]

    total_collisions = []
    advisories = []
    total_claims_count = 0

    for fa in agent_a_files:
        stem_a = fa.stem.replace("agent_a_", "")
        fb_matches = [f for f in agent_b_files if f.stem.replace("agent_b_", "") == stem_a]
        if not fb_matches:
            continue
        fb = fb_matches[0]

        source_a = fa.read_text(encoding="utf-8")
        source_b = fb.read_text(encoding="utf-8")

        claims_a = extract_claims(source_a, agent_id="agent_a")
        claims_b = extract_claims(source_b, agent_id="agent_b")
        total_claims_count += len(claims_a) + len(claims_b)

        cols = detect_collisions(claims_a, claims_b)
        total_collisions.extend(cols)
        for c in cols:
            advisories.append(generate_advisory(c))

    max_sev = max((c.severity for c in total_collisions), default=0.0)

    return {
        "type": "TELEMETRY_UPDATE",
        "timestamp": time.strftime("%H:%M:%S"),
        "active_collisions": len(total_collisions),
        "max_severity": round(max_sev, 2),
        "total_claims": total_claims_count,
        "collisions": [
            {
                "symbol": col.claim_a.symbol,
                "claim_a": col.claim_a.domain,
                "claim_b": col.claim_b.domain,
                "collision_class": col.collision_class.upper(),
                "severity": col.severity,
                "status": col.status.value,
                "halted": col.halted,
            }
            for col in total_collisions
        ],
        "advisories": [
            {
                "symbol": adv.vector.claim_a.symbol,
                "target_agent": adv.target_agent,
                "recommended_action": adv.recommended_action,
                "patch_hint": adv.patch_hint,
                "severity": adv.vector.severity,
            }
            for adv in advisories
        ],
    }


class TelemetryBroadcaster:
    """Async WebSocket server that broadcasts AssumptionLedger and collision events."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765, watch_path: Path | None = None) -> None:
        self.host = host
        self.port = port
        self.watch_path = watch_path or Path("tests/fixtures")
        self._clients: Set[Any] = set()
        self._server: Any = None

    async def register(self, websocket: Any) -> None:
        """Register a new UI client connection and push the latest telemetry frame immediately."""
        self._clients.add(websocket)
        logger.info(f"UI console connected. Active listeners: {len(self._clients)}")
        # Send initial snapshot immediately upon connection
        payload = _compute_telemetry_payload(self.watch_path)
        await websocket.send(json.dumps(payload))

    async def unregister(self, websocket: Any) -> None:
        """Unregister a disconnected UI client."""
        self._clients.discard(websocket)
        logger.info(f"UI console disconnected. Active listeners: {len(self._clients)}")

    async def broadcast_payload(self, payload: dict[str, Any]) -> None:
        """Fan-out a structured JSON telemetry frame to all connected UI clients."""
        if not self._clients:
            return

        message = json.dumps(payload, default=str)
        disconnected = set()

        for client in self._clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)

        for client in disconnected:
            self._clients.discard(client)

    async def handler(self, websocket: Any, *args: Any, **kwargs: Any) -> None:
        """WebSocket connection handler loop."""
        await self.register(websocket)
        try:
            async for raw_msg in websocket:
                try:
                    data = json.loads(raw_msg)
                    if data.get("action") == "REQUEST_TELEMETRY":
                        payload = _compute_telemetry_payload(self.watch_path)
                        await websocket.send(json.dumps(payload))
                except json.JSONDecodeError:
                    pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

    async def watch_loop(self) -> None:
        """Periodically check for disk changes and push telemetry frames."""
        last_hash = ""
        while True:
            try:
                files = list(self.watch_path.glob("*.py"))
                current_hash = "".join(f"{f.name}:{f.stat().st_mtime}" for f in sorted(files))
                if current_hash != last_hash:
                    last_hash = current_hash
                    payload = _compute_telemetry_payload(self.watch_path)
                    await self.broadcast_payload(payload)
            except Exception as e:
                logger.warning(f"Error in telemetry watch loop: {e}")
            await asyncio.sleep(0.5)

    async def start(self) -> None:
        """Start the async WebSocket broadcast daemon."""
        self._server = await websockets.serve(self.handler, self.host, self.port)
        logger.info(f"CROSSFIRE Broadcaster listening at ws://{self.host}:{self.port}")
        await self.watch_loop()

    async def stop(self) -> None:
        """Stop the WebSocket server cleanly."""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
