from aiogram         import Router
from aiogram.filters import CommandStart
from aiogram.types   import Message, ReplyKeyboardMarkup, KeyboardButton
from settings        import settings

import websockets
import logging

router = Router()

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
    if (message.chat.id in settings.users):
        print(settings.url)
        uri = f"ws://{settings.url}/ws/chat"
        async with websockets.connect(uri) as websocket:
            await websocket.send(message.text)
    else:
        await message.delete()
