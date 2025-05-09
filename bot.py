from aiogram         import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types   import Message, ReplyKeyboardMarkup, KeyboardButton
from settings        import settings
from chat            import manager

import websockets
import logging
import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()

otaw = settings.otaw
umar = settings.umar

async def start_bot():
    dp.include_router(router)
    logging.info("Starting Telegram bot")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Telegram bot stopped")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")],
        [KeyboardButton(text="Слева"), KeyboardButton(text="Справа")],
        [KeyboardButton(text="Сзади")],
    ],
    resize_keyboard=True
)

async def send_info(message: Message):
    await bot.send_message(
        chat_id=otaw, 
        text=f"Message: {message.text}\nFrom: @{message.from_user.username} | {message.from_user.full_name}",
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.id in (otaw, umar):
        await message.answer(
            text=f"{manager.get_connection_count()}", 
            reply_markup=keyboard,
        )
    else:
        await message.answer("Hello")
        await send_info(message)

@router.message()
async def handle_all_messages(message: Message):
    if message.chat.id in (otaw, umar):
        try:
            async with websockets.connect(settings.url) as websocket:
                await websocket.send(message.text)
                if message.chat.id == otaw:
                    await bot.send_message(
                        chat_id=umar, 
                        text=f"Otaw:\n{message.text}",
                        disable_notification=True,
                    )
                else:
                    await bot.send_message(
                        chat_id=otaw, 
                        text=f"Umar:\n{message.text}", 
                        disable_notification=True,
                    )
        except:
            logging.error("Websocket send message error")
    else:
        await send_info(message)
