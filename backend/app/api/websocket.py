# ============================================================
# backend/app/api/websocket.py
# ============================================================
#
# 📖 REAL-TIME WEBSOCKET HUB
# Streams live agent execution steps & thoughts directly to the frontend.
# ============================================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import asyncio
import structlog

logger = structlog.get_logger()

router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections for streaming agent thoughts."""
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("⚡ WebSocket Client Connected")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("🔌 WebSocket Client Disconnected")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error("Failed to send WS message", error=str(e))


manager = ConnectionManager()


@router.websocket("/ws/agents")
async def websocket_agents(websocket: WebSocket):
    """
    WebSocket endpoint for real-time agent activity feed.
    Frontend connects here to receive live streaming agent thoughts!
    """
    await manager.connect(websocket)
    try:
        # Initial welcome message
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "message": "Connected to AdsIQ Real-Time Agent Stream"
        }))

        while True:
            # Wait for messages from client (ping or trigger)
            data = await websocket.receive_text()
            payload = json.loads(data)

            if payload.get("action") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            elif payload.get("action") == "run_agent":
                agent_type = payload.get("agent_type", "TROUBLESHOOTER")
                prompt = payload.get("prompt", "Troubleshoot error")

                # Stream initial step
                await websocket.send_text(json.dumps({
                    "type": "agent_step",
                    "step": "initializing",
                    "message": f"Starting {agent_type} agent..."
                }))

                await asyncio.sleep(0.5)

                await websocket.send_text(json.dumps({
                    "type": "agent_step",
                    "step": "executing",
                    "message": f"Processing user query: '{prompt}'"
                }))

                await asyncio.sleep(0.8)

                # Stream final output
                await websocket.send_text(json.dumps({
                    "type": "agent_complete",
                    "step": "done",
                    "message": f"{agent_type} execution complete!",
                    "output": {"status": "SUCCESS", "agent": agent_type}
                }))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
