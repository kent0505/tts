from aiogram         import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types   import Message, ReplyKeyboardMarkup, KeyboardButton
from core.settings   import settings

import websockets
import logging
import asyncio

bot = Bot(token=settings.token)
dp = Dispatcher()
router = Router()

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

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello", reply_markup=keyboard)

@router.message()
async def handle_all_messages(message: Message):
    id = message.chat.id
    text = message.text
    otaw = settings.otaw
    umar = settings.umar

    if id in (otaw, umar):
        uri = f"wss://{settings.url}/ws/chat"
        async with websockets.connect(uri) as websocket:
            await websocket.send(text)
            if id == otaw:
                await bot.send_message(
                    chat_id=umar, 
                    text=f'Otaw: {text}',
                    disable_notification=True,
                )
            else:
                await bot.send_message(
                    chat_id=otaw, 
                    text=f'Umar: {text}', 
                    disable_notification=True,
                )
    else:
        await bot.send_message(
            chat_id=otaw, 
            text=f'Message:\n{text}\nFrom:\n{message.from_user.username}\n{message.from_user.full_name}'
        )
        await message.delete()
