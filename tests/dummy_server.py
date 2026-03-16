import asyncio
import websockets
import json

rooms = {}

async def handle_client(websocket):
    print(f"[SERVER] New connection from {websocket.remote_address}")
    my_rooms = set() 

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print("[SERVER] Error: Received message is not valid JSON.")
                continue 

            action = data.get("action")
            room_name = data.get("room")

            if action == "join" and room_name:
                if room_name not in rooms:
                    rooms[room_name] = set()
                
                rooms[room_name].add(websocket)
                my_rooms.add(room_name)
                print(f"[SERVER] User joined room: {room_name}")
                
                success_msg = json.dumps({"status": "success", "message": f"Joined {room_name}"})
                await websocket.send(success_msg)

            elif action == "message" and room_name:
                if room_name in rooms:
                    content = data.get("content", "")
                    
                    outgoing_msg = json.dumps({
                        "room": room_name,
                        "content": content
                    })
                    
                    websockets.broadcast(rooms[room_name], outgoing_msg)
                    print(f"[SERVER] Broadcasted to {room_name}: {content}")

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        for room in my_rooms:
            if websocket in rooms[room]:
                rooms[room].remove(websocket)
                if len(rooms[room]) == 0:
                    del rooms[room]
        print(f"[SERVER] User disconnected and cleaned up.")

async def main():
    print("[SERVER] Starting JSON Room Server on ws://localhost:8765")
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())