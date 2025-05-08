import asyncio
import websockets
import pyttsx3

engine = pyttsx3.init()

async def listen_once():
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

async def main():
    while True:
        try:
            await listen_once()
        except:
            print("Error")
        print("Reconnecting in 5 seconds...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exited by user.")
