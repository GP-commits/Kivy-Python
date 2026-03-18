import asyncio
import json
import websockets

connected_clients: dict = {}
_counter = 0

def _next_id() -> str:
    global _counter
    _counter += 1
    return f"user{_counter}"

async def _send(ws, payload: dict):
    try:
        await ws.send(json.dumps(payload))
    except Exception:
        pass

async def handle_client(websocket):
    client_id = _next_id()
    connected_clients[websocket] = client_id
    print(f"[DUMMY] {client_id} connected  (total: {len(connected_clients)})")

    await _send(websocket, {"type": "welcome", "client_id": client_id})

    try:
        async for raw in websocket:
            print(f"[DUMMY] {client_id} → {raw}")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await _send(websocket, {"type": "error", "message": "Invalid JSON"})
                continue

            action  = data.get("action")
            room    = data.get("room", "lobby")
            content = data.get("content", "")

            if action == "join":
                await _send(websocket, {"type": "joined", "room": room, "status": "success"})

            elif action == "message" and content:
                payload = {
                    "type":      "message",
                    "room":      room,
                    "sender_id": client_id,
                    "content":   content,
                }
                for ws in list(connected_clients):
                    await _send(ws, payload)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.pop(websocket, None)
        print(f"[DUMMY] {client_id} disconnected  (total: {len(connected_clients)})")

async def main():
    print("[DUMMY SERVER] Starting on ws://localhost:8765")
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())