import asyncio
import websockets
import pyttsx3

engine = pyttsx3.init()

async def listen():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server.")
        while True:
            try:
                message = await websocket.recv()
                print(f"Received: {message}")
                engine.say(message)
                engine.runAndWait()
            except websockets.ConnectionClosed:
                print("Connection closed.")
                break

if __name__ == "__main__":
    asyncio.run(listen())
