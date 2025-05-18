from aiogram import Router, F
from aiogram.types import Message
from pathlib import Path

router = Router()

HELP_DIR = Path(__file__).parent.parent / "help"

def read_help(name: str) -> str | None:
    path = HELP_DIR / f"{name}.md"
    return path.read_text(encoding="utf-8") if path.exists() else None

@router.message(F.text == "/help_magic_code")
async def help_magic_code(message: Message):
    text = read_help("magic_code")
    if text:
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("❗ Справка по /magic_code пока недоступна.")

@router.message(F.text == "/help_generator_clients")
async def help_generator_clients(message: Message):
    text = read_help("generator_clients")
    if text:
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("❗ Справка по /generator_clients пока недоступна.")
