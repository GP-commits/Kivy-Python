import asyncio
import websockets
import json
import pytest

URI = "ws://localhost:8765"
    
@pytest.mark.asyncio
async def test_room_join_and_message():
    async with websockets.connect(URI) as ws:
        join_cmd = {"action": "join", "room": "lobby"}
        await ws.send(json.dumps(join_cmd))
    
        raw_resp = await ws.recv()
        resp = json.loads(raw_resp)
        assert resp["status"] == "success"

        msg_cmd = {"action": "message", "room": "lobby", "content": "Hello Team!"}
        await ws.send(json.dumps(msg_cmd))
        
        raw_broadcast = await ws.recv()
        broadcast = json.loads(raw_broadcast)
        assert broadcast["room"] == "lobby"
        assert broadcast["content"] == "Hello Team!"

@pytest.mark.asyncio
async def test_stress_multi_room_routing():
    """Stress test: 50 clients in different rooms should only hear their own room's noise."""
    
    async def fake_client_task(client_id):
        room_name = "room_A" if client_id % 2 == 0 else "room_B"
        
        async with websockets.connect(URI) as ws:
            await ws.send(json.dumps({"action": "join", "room": room_name}))
            await ws.recv()
            
            test_content = f"Message from {client_id}"
            await ws.send(json.dumps({"action": "message", "room": room_name, "content": test_content}))
            
            raw_data = await ws.recv()
            data = json.loads(raw_data)
            
            assert data["room"] == room_name
            assert test_content in data["content"]

    tasks = [fake_client_task(i) for i in range(50)]
    await asyncio.gather(*tasks)