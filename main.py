from fastapi    import FastAPI, WebSocket, WebSocketDisconnect
from aiogram    import Bot, Dispatcher
from contextlib import asynccontextmanager
from dotenv     import load_dotenv
from typing     import List
from bot        import router
from settings   import settings

import logging
import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()

async def start_bot():
    dp.include_router(router)
    logging.info("Starting Telegram bot")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Telegram bot stopped")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logging.info("STARTUP")
    bot_task = asyncio.create_task(start_bot())
    yield
    # shutdown
    logging.info("SHUTDOWN")
    bot_task.cancel()

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters=settings.swagger,
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.route("/")
async def main():
    return {"message": "OK"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# python -m venv venv
# venv\Scripts\activate
# source venv/bin/activate
# pip install -r requirements.txt
# uvicorn main:app --reload
