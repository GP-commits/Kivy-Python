import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    print(f"[SERVER] New user joined! Total users: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            print(f"[SERVER] Received: {message}")
            
            websockets.broadcast(connected_clients, f"Broadcast: {message}")
            
    except websockets.exceptions.ConnectionClosed:
        pass    
    finally:
        connected_clients.remove(websocket)
        print(f"[SERVER] User left. Total users: {len(connected_clients)}")

async def main():
    print("[SERVER] Starting on port 8765") #ws://localhost:8765
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())