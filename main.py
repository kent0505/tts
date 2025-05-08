from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

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

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# from fastapi                 import FastAPI
# from fastapi.staticfiles     import StaticFiles
# from contextlib              import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logging.basicConfig(level=logging.INFO)
#     await create_tables()
#     yield

# app = FastAPI(
#     lifespan=lifespan,
#     swagger_ui_parameters={"defaultModelsExpandDepth": -1},
# )

# app.mount(app=StaticFiles(directory="static"),    path="/static")
# app.mount(app=StaticFiles(directory="templates"), path="/templates")

# app.include_router(clover_home_router, include_in_schema=False)
# app.include_router(parser_router, prefix="/api/v1/parser", tags=["Parser"])

# python -m venv venv
# venv\Scripts\activate
# source venv/bin/activate
# pip install -r requirements.txt
# uvicorn src.main:app --reload
# alembic revision --autogenerate -m ""
# alembic upgrade head
