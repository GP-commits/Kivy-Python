# Kivy Network 🌐

[![PyPI version](https://img.shields.io/pypi/v/kivy-network.svg)](https://pypi.org/project/kivy-network/)
[![Python versions](https://img.shields.io/pypi/pyversions/kivy-network.svg)](https://pypi.org/project/kivy-network/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A robust, asynchronous, real-time WebSocket networking engine specifically designed for **Kivy** applications.

Building real-time multiplayer games, chat applications, or live dashboards in Kivy can be tricky because blocking network calls freeze the Kivy UI thread. `kivy-network` solves this by bridging the gap between Python's `asyncio` WebSockets and Kivy's 60FPS `Clock`, ensuring your app stays perfectly smooth.

## Features

- **Thread-Safe UI Updates:** Safely routes background network events into Kivys main thread using `Clock.schedule_once`.
- **Indestructible Client:** Built-in auto-reconnect engine with backoff. Survives network drops, tunnels, and server reboots automatically.
- **Pro-Level Typing:** Uses strict Python `dataclasses` (`NetworkMessage`) for full IDE autocomplete support. Say goodbye to dictionary typo bugs.
- **Ghost Hunter:** Built-in Ping/Pong heartbeat system safely cleans up dead or half-open connections.
- **Lightweight:** Minimal dependencies. Built purely on standard `websockets` and Kivy.

---

## Installation

Install via `pip` or `uv`:

```bash
pip install kivy-network
```

_(Note: Ensure you have Kivy installed and configured for your operating system)._

---

## Quick Start

### 1. The Kivy Client

Here is how easy it is to drop `kivy-network` into your application.

```python
import asyncio
from kivy.app import App
from kivy.uix.label import Label
from kivy-network.network_client import RealTimeClient

class MultiplayerApp(App):
    def build(self):
        self.label = Label(text="Connecting...")

        self.network = RealTimeClient("ws://localhost:8765")

        self.network.bind(on_connected=self.on_connect)
        self.network.bind(on_message=self.on_message)
        self.network.bind(on_disconnected=self.on_disconnect)

        asyncio.create_task(self.network.run_forever())

        return self.label

    def on_connect(self, instance):
        self.label.text = "Connected! Joining room..."
        asyncio.create_task(self.network.join_room("lobby"))

    def on_message(self, instance, message):
        if message.type == "message":
            self.label.text = f"User {message.sender_id} says: {message.content}"

    def on_disconnect(self, instance):
        self.label.text = "Connection lost. Reconnecting..."

if __name__ == "__main__":
    asyncio.run(MultiplayerApp().async_run(async_lib='asyncio'))
```

### 2. The NetworkMessage API

Every time your UI receives an `on_message` event, it receives a strictly-typed `NetworkMessage` dataclass with the following properties available for autocomplete:

- `message.type` (str) - E.g., 'welcome', 'message', 'admin'
- `message.room` (str | None)
- `message.content` (str | None)
- `message.sender_id` (str | None)
- `message.raw_data` (dict) - The raw JSON payload fallback.

---

## Running a Test Server

`kivy-network` connects seamlessly to any standard WebSocket server.

We recommend spinning up a quick python server using the `websockets` library:

```python
import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
```

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

```

```
