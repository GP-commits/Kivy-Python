import asyncio
import websockets
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any
from kivy.event import EventDispatcher
from kivy.clock import Clock

@dataclass
class NetworkMessage:
    type: str               
    room: Optional[str]     
    content: Optional[str] 
    sender_id: Optional[str] 
    raw_data: Dict[str, Any] 

class NetworkEventDispatcher(EventDispatcher):
    __events__ = ('on_connected', 'on_message', 'on_error', 'on_disconnected')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_connected(self, *args): pass
    def on_message(self, message: NetworkMessage): pass 
    def on_error(self, error_msg: str): pass
    def on_disconnected(self, *args): pass

    def trigger_message_safely(self, message_obj: NetworkMessage):
        Clock.schedule_once(lambda dt: self.dispatch('on_message', message_obj), 0)

    def trigger_connected_safely(self):
        Clock.schedule_once(lambda dt: self.dispatch('on_connected'), 0)

    def trigger_error_safely(self, error_msg: str):
        Clock.schedule_once(lambda dt: self.dispatch('on_error', error_msg), 0)
        
    def trigger_disconnected_safely(self):
        Clock.schedule_once(lambda dt: self.dispatch('on_disconnected'), 0)


class RealTimeClient(NetworkEventDispatcher):
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
                    self.trigger_connected_safely()
                    await self._listen()
                    
            except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError):
                self.connected = False
                self.trigger_disconnected_safely()
                self.trigger_error_safely("Connection dropped.")
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_delay)
            except Exception as e:
                print(f"[CLIENT] Critical Error: {e}")
                await asyncio.sleep(5)

    async def _listen(self) -> None:
        async for message in self.websocket:
            data = json.loads(message)
            
            if data.get("type") == "welcome":
                self.client_id = data.get("client_id")
            else:
                msg_obj = NetworkMessage(
                    type=data.get("type", "unknown"),
                    room=data.get("room"),
                    content=data.get("content"),
                    sender_id=data.get("sender_id"),
                    raw_data=data
                )
                self.trigger_message_safely(msg_obj)

    async def join_room(self, room_name: str) -> None:
        if self.connected and self.websocket:
            data = {"action": "join", "room": room_name}
            await self.websocket.send(json.dumps(data))

    async def send_chat(self, room_name: str, content: str) -> None:
        if self.connected and self.websocket:
            data = {"action": "message", "room": room_name, "content": content}
            await self.websocket.send(json.dumps(data))