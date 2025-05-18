from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

router = Router()

@router.message(F.text == "/generator_clients")
async def open_generator_clients(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🧲 Открыть генератор",
                web_app=WebAppInfo(url="https://simoronator.ru/apps/generator_clients/")
            )]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "✨ Готово! Нажми кнопку ниже, чтобы запустить генератор клиентов:",
        reply_markup=keyboard
    )
