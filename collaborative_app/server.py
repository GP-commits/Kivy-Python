import asyncio
import websockets
import json

# A set of all connected clients
connected_clients = set()

async def handler(websocket):
    # Register client
    connected_clients.add(websocket)
    try:
        # Send a welcome message
        await websocket.send(json.dumps({
            "type": "welcome",
            "client_id": str(id(websocket))
        }))
        
        # Listen for messages
        async for message in websocket:
            # Parse it just to make sure it's valid JSON
            try:
                data = json.loads(message)
                print(f"Received: {data}")
                
                # Broadcast the message to all OTHER clients
                for client in connected_clients:
                    if client != websocket:
                        await client.send(message)
            except ValueError:
                pass
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket Broadcast Server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
