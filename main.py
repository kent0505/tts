from fastapi       import FastAPI
from contextlib    import asynccontextmanager
from dotenv        import load_dotenv
from bot.bot       import start_bot
from core.settings import settings
from routers.home  import router as home_router
from chat.chat     import router as chat_router

import logging
import asyncio

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

app.include_router(home_router)
app.include_router(chat_router, include_in_schema=False)

# python -m venv venv
# venv\Scripts\activate
# source venv/bin/activate
# pip install -r requirements.txt
# uvicorn main:app --reload
