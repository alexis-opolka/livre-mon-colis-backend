#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:

        await websocket.send("test data")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())