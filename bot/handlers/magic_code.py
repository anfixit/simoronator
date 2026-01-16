"""
Обработчик команды /magic_code - Волшебный калькулятор Симорон.

Генерирует персональный магический код на основе намерения
и личных данных пользователя.
"""
import logging

import yaml
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from constants import (
    ERROR_GENERIC,
    MIN_FIO_WORDS,
    PARSE_MODE_MARKDOWN,
    TEXTS_DIR,
)
from utils.magic_encoder import encode_magic_code

router = Router()
logger = logging.getLogger(__name__)

# Загрузка текстов из YAML
TEXTS_PATH = TEXTS_DIR / "magic_code.yml"

try:
    with open(TEXTS_PATH, "r", encoding="utf-8") as f:
        TEXTS = yaml.safe_load(f)
except FileNotFoundError:
    logger.error(f"Файл текстов не найден: {TEXTS_PATH}")
    TEXTS = {}
except yaml.YAMLError as e:
    logger.error(f"Ошибка парсинга YAML: {e}")
    TEXTS = {}


class MagicCodeStates(StatesGroup):
    """Состояния FSM для ритуала магического кода."""

    waiting_for_intent = State()
    waiting_for_fio_birthdate = State()


@router.message(F.text.lower() == "/magic_code")
async def start_magic_code(
    message: Message,
    state: FSMContext
) -> None:
    """
    Начало ритуала генерации магического кода.

    Args:
        message: Сообщение от пользователя
        state: Контекст состояния FSM
    """
    try:
        text = TEXTS.get("start", {}).get(
            "ask_intent",
            "🔮 Напиши своё намерение."
        )
        await message.answer(text)
        await state.set_state(MagicCodeStates.waiting_for_intent)
        logger.info(
            f"Пользователь {message.from_user.id} "
            f"начал ритуал magic_code"
        )
    except Exception as e:
        logger.error(f"Ошибка в start_magic_code: {e}")
        await message.answer(ERROR_GENERIC)


@router.message(MagicCodeStates.waiting_for_intent)
async def get_intent(message: Message, state: FSMContext) -> None:
    """
    Получение намерения от пользователя.

    Args:
        message: Сообщение с намерением
        state: Контекст состояния FSM
    """
    try:
        await state.update_data(intent=message.text.strip())
        text = TEXTS.get("start", {}).get(
            "ask_identity",
            "✍️ Теперь укажи ФИО и дату рождения."
        )
        await message.answer(text)
        await state.set_state(
            MagicCodeStates.waiting_for_fio_birthdate
        )
        logger.info(
            f"Пользователь {message.from_user.id} "
            f"указал намерение"
        )
    except Exception as e:
        logger.error(f"Ошибка в get_intent: {e}")
        await message.answer(ERROR_GENERIC)


@router.message(MagicCodeStates.waiting_for_fio_birthdate)
async def get_fio_and_generate(
    message: Message,
    state: FSMContext
) -> None:
    """
    Получение ФИО и даты рождения, генерация кода.

    Args:
        message: Сообщение с ФИО и датой рождения
        state: Контекст состояния FSM
    """
    try:
        data = await state.get_data()
        intent = data.get("intent", "")
        user_input = message.text.strip()

        if len(user_input.split()) < MIN_FIO_WORDS:
            bad_format = TEXTS.get("start", {}).get(
                "bad_format",
                "⚠️ Укажи ФИО и дату рождения."
            )
            await message.answer(bad_format)
            return

        full_text = f"{intent} {user_input}"
        code = encode_magic_code(full_text, compress=True)

        result_prefix = TEXTS.get("complete", {}).get(
            "result_prefix",
            "✨ Твой ЛИЧНЫЙ ВОЛШЕБНЫЙ КОД СИМОРОН:"
        )
        result_suffix = TEXTS.get("complete", {}).get(
            "result_suffix",
            "📜 Нанеси его на бумагу или запомни."
        )

        await message.answer(
            f"{result_prefix}\n\n`{code}`\n\n{result_suffix}",
            parse_mode=PARSE_MODE_MARKDOWN
        )

        await state.clear()
        logger.info(
            f"Пользователь {message.from_user.id} "
            f"получил код: {code}"
        )

    except Exception as e:
        logger.error(f"Ошибка в get_fio_and_generate: {e}")
        await message.answer(ERROR_GENERIC)
        await state.clear()
