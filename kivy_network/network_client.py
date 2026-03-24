import asyncio
import websockets
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any

# FIX 1: Corrected import path
from kivy_network.events import NetworkDispatcher


@dataclass
class NetworkMessage:
    type: str
    room: Optional[str]
    content: Optional[str]
    sender_id: Optional[str]
    raw_data: Dict[str, Any]


class RealTimeClient(NetworkDispatcher):
    def __init__(self, uri: str = "ws://localhost:8765", **kwargs):
        super().__init__(**kwargs)
        self.uri = uri
        self.websocket = None
        self.client_id: Optional[str] = None
        self.connected: bool = False
        self.reconnect_delay: int = 1
        self.max_delay: int = 15

    async def run_forever(self) -> None:
        while True:
            try:
                print(f"[CLIENT] Attempting to connect to {self.uri}...")
                async with websockets.connect(self.uri) as ws:
                    self.websocket = ws
                    self.connected = True
                    self.reconnect_delay = 1

                    self.trigger_event_safely("on_connected")

                    await self._listen()

            except (
                websockets.exceptions.ConnectionClosedError,
                ConnectionRefusedError,
            ):
                self.connected = False

                self.trigger_event_safely("on_disconnected")
                self.trigger_event_safely("on_error", "Connection dropped.")

                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_delay)
            except Exception as e:
                print(f"[CLIENT] Critical Error: {e}")
                await asyncio.sleep(5)

    async def _listen(self) -> None:
        async for message in self.websocket:
            # FIX 2: Fixed the indentation alignment here!
            try:
                data = json.loads(message)

                if not isinstance(data, dict):
                    raise ValueError(
                        "Payload is a valid JSON format, but not a dictionary object."
                    )

                if data.get("type") == "welcome":
                    self.client_id = data.get("client_id")
                    print(f"[CLIENT] Server assigned ID: {self.client_id}")
                else:
                    msg_obj = NetworkMessage(
                        type=data.get("type", "unknown"),
                        room=data.get("room"),
                        content=data.get("content"),
                        sender_id=data.get("sender_id"),
                        raw_data=data,
                    )
                    self.trigger_event_safely("on_message_received", msg_obj)

            except json.JSONDecodeError:
                print(f"[CLIENT - CHAOS SHIELD] Blocked malformed JSON: {message}")
                self.trigger_event_safely("on_error", "Ignored corrupted data packet.")

            except ValueError as ve:
                print(f"[CLIENT - CHAOS SHIELD] Blocked invalid structure: {ve}")
                self.trigger_event_safely("on_error", "Ignored invalid data structure.")

            except Exception as e:
                print(
                    f"[CLIENT - CHAOS SHIELD] Unexpected error processing message: {e}"
                )

    async def join_room(self, room: str) -> None:
        if self.connected and self.websocket:
            payload = {"action": "join", "room": room}
            await self.websocket.send(json.dumps(payload))

    async def send_chat(self, room: str, content: str) -> None:
        if self.connected and self.websocket:
            payload = {"action": "message", "room": room, "content": content}
            await self.websocket.send(json.dumps(payload))
