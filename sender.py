import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        message = "Привет"
        await websocket.send(message)

if __name__ == "__main__":
    asyncio.run(send_message())
