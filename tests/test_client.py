import asyncio
import websockets
import pytest

uri = "ws://localhost:8765"

@pytest.mark.asyncio
async def test_single_client():
    async with websockets.connect(uri) as ws:
        await ws.send("Hello from Test 1")
        response = await ws.recv()
        assert "Broadcast: Hello from Test 1" in response

@pytest.mark.asyncio
async def test_50_clients(): # stress testing with 50 clients
    async def fake_client_task(client_id):
        async with websockets.connect(uri) as ws:
            await ws.send(f"Stress test message {client_id}")
            response = await ws.recv()
            assert "Broadcast:" in response

    tasks = [fake_client_task(i) for i in range(50)]
    await asyncio.gather(*tasks) # runninng all 50 clients at the same time :)