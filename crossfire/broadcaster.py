"""WebSocket broadcaster streaming CROSSFIRE telemetry and radar states to the UI console."""

import asyncio
import json
import logging
from typing import Any, Set
import websockets

logger = logging.getLogger("crossfire.broadcaster")


class TelemetryBroadcaster:
    """Async WebSocket server that broadcasts AssumptionLedger and collision events."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765) -> None:
        self.host = host
        self.port = port
        self._clients: Set[Any] = set()
        self._server: Any = None

    async def register(self, websocket: Any) -> None:
        """Register a new UI client connection."""
        self._clients.add(websocket)
        logger.info(f"UI console connected. Active listeners: {len(self._clients)}")
        # Send initial handshake frame
        await websocket.send(
            json.dumps({
                "type": "HEARTBEAT",
                "status": "ONLINE",
                "radar": "STANDBY",
            })
        )

    async def unregister(self, websocket: Any) -> None:
        """Unregister a disconnected UI client."""
        self._clients.discard(websocket)
        logger.info(f"UI console disconnected. Active listeners: {len(self._clients)}")

    async def broadcast(self, event_type: str, payload: dict[str, Any]) -> None:
        """Fan-out a structured JSON telemetry frame to all connected UI clients."""
        if not self._clients:
            return

        message = json.dumps({"type": event_type, "payload": payload}, default=str)
        disconnected = set()

        for client in self._clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)

        for client in disconnected:
            self._clients.discard(client)

    async def handler(self, websocket: Any, path: str = "/") -> None:
        """WebSocket connection handler loop."""
        await self.register(websocket)
        try:
            async for raw_msg in websocket:
                # Handle client command toggles (e.g. simulated resolution)
                try:
                    data = json.loads(raw_msg)
                    if data.get("action") == "REQUEST_RADAR_STATUS":
                        await websocket.send(json.dumps({"type": "STATUS_PONG", "ok": True}))
                except json.JSONDecodeError:
                    pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

    async def start(self) -> None:
        """Start the async WebSocket broadcast daemon."""
        self._server = await websockets.serve(self.handler, self.host, self.port)
        logger.info(f"CROSSFIRE Broadcaster listening at ws://{self.host}:{self.port}")

    async def stop(self) -> None:
        """Stop the WebSocket server cleanly."""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
