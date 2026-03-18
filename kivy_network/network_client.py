import asyncio
import websockets
import json

class RealTimeClient:
    def __init__(self, uri="ws://localhost:8765"):
        self.uri = uri
        self.websocket = None
        self.client_id = None
        self.connected = False

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            print(f"[CLIENT] Successfully connected to {self.uri}")
        except Exception as e:
            print(f"[CLIENT] Connection failed: {e}")

    async def listen(self):
        if not self.websocket:
            print("[CLIENT] Error: Call connect() first.")
            return

        try:
            async for message in self.websocket:
                data = json.loads(message)
                
                if data.get("type") == "welcome":
                    self.client_id = data.get("client_id")
                    print(f"[CLIENT] Server gave me ID: {self.client_id}")
                else:
                    print(f"[CLIENT] Incoming Data: {data}")

        except websockets.exceptions.ConnectionClosed:
            print("[CLIENT] Connection closed by the server.")
            self.connected = False

    async def join_room(self, room_name):
        data = {"action": "join", "room": room_name}
        await self.websocket.send(json.dumps(data))

    async def send_chat(self, room_name, content):
        data = {"action": "message", "room": room_name, "content": content}
        await self.websocket.send(json.dumps(data))

async def test_engine():
    client = RealTimeClient()
    await client.connect()
    asyncio.create_task(client.listen())
    await asyncio.sleep(0.5)
    print("\n--- Test ---")
    await client.join_room("lobby")
    await asyncio.sleep(0.5) 
    await client.send_chat("lobby", "Message from Client Engine")
    await asyncio.sleep(5)
    print("\n[CLIENT] Shutting down test.")

if __name__ == "__main__":
    asyncio.run(test_engine())