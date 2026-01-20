"""
Обработчик команды /matrix_message - Matrix Message.

Отправка магических сообщений в Матрицу реальности.
"""
import logging
import random

import yaml
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from config import Config
from constants import (
    BTN_OPEN_MATRIX,
    ERROR_GENERIC,
    ERROR_WEBAPP,
    MSG_WEBAPP_READY,
    PARSE_MODE_HTML,
    TEXTS_DIR,
    WEBAPP_PATHS,
)

router = Router()
logger = logging.getLogger(__name__)

# Загрузка текстов из YAML
TEXTS_PATH = TEXTS_DIR / "matrix_message.yml"

try:
    with open(TEXTS_PATH, "r", encoding="utf-8") as f:
        TEXTS = yaml.safe_load(f)
except FileNotFoundError:
    logger.error(f"Файл текстов не найден: {TEXTS_PATH}")
    TEXTS = {}
except yaml.YAMLError as e:
    logger.error(f"Ошибка парсинга YAML: {e}")
    TEXTS = {}


class MatrixMessageStates(StatesGroup):
    """Состояния FSM для Matrix Message."""

    waiting_for_message = State()


@router.message(F.text.lower() == "/matrix_message")
async def matrix_message_menu(message: Message) -> None:
    """
    Меню выбора режима работы Matrix Message.

    Args:
        message: Сообщение от пользователя
    """
    try:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✨ Красивая версия (PWA)",
                        callback_data="matrix_message_pwa"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⚡ Быстро в боте",
                        callback_data="matrix_message_bot"
                    )
                ]
            ]
        )

        await message.answer(
            "📡 <b>Matrix Message</b>\n\n"
            "Отправка сообщений напрямую в Матрицу.\n\n"
            "Выбери способ запуска:",
            reply_markup=keyboard,
            parse_mode=PARSE_MODE_HTML
        )

        logger.info(
            f"Пользователь {message.from_user.id} "
            f"открыл меню matrix_message"
        )

    except Exception as e:
        logger.error(f"Ошибка в matrix_message_menu: {e}")
        await message.answer(ERROR_GENERIC)


@router.callback_query(F.data == "matrix_message_pwa")
async def open_matrix_message_pwa(
    callback,
    config: Config
) -> None:
    """
    Открытие PWA приложения Matrix Message.

    Args:
        callback: Callback query
        config: Объект конфигурации приложения
    """
    try:
        webapp_url = (
            f"{config.webapp.base_url}"
            f"{WEBAPP_PATHS['matrix_message']}"
        )

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text=BTN_OPEN_MATRIX,
                        web_app=WebAppInfo(url=webapp_url)
                    )
                ]
            ],
            resize_keyboard=True
        )

        await callback.message.edit_text(MSG_WEBAPP_READY)
        await callback.message.answer(
            "Нажми кнопку ниже:",
            reply_markup=keyboard
        )

        await callback.answer()

        logger.info(
            f"Пользователь {callback.from_user.id} "
            f"открыл matrix_message PWA: {webapp_url}"
        )

    except Exception as e:
        logger.error(f"Ошибка в open_matrix_message_pwa: {e}")
        await callback.message.answer(ERROR_WEBAPP)
        await callback.answer()


@router.callback_query(F.data == "matrix_message_bot")
async def start_matrix_message_bot(
    callback,
    state: FSMContext
) -> None:
    """
    Начало ритуала Matrix Message в боте.

    Args:
        callback: Callback query
        state: Контекст состояния FSM
    """
    try:
        text = TEXTS.get("start", {}).get(
            "ask_message",
            "📡 Напиши своё послание Матрице:"
        )

        await callback.message.edit_text(
            text,
            parse_mode=PARSE_MODE_HTML
        )
        await state.set_state(MatrixMessageStates.waiting_for_message)
        await callback.answer()

        logger.info(
            f"Пользователь {callback.from_user.id} "
            f"начал matrix_message в боте"
        )

    except Exception as e:
        logger.error(f"Ошибка в start_matrix_message_bot: {e}")
        await callback.message.answer(ERROR_GENERIC)
        await callback.answer()


@router.message(MatrixMessageStates.waiting_for_message)
async def process_matrix_message(
    message: Message,
    state: FSMContext
) -> None:
    """
    Обработка сообщения для Матрицы.

    Args:
        message: Сообщение от пользователя
        state: Контекст состояния FSM
    """
    try:
        # Сообщение об отправке
        confirm_text = TEXTS.get("start", {}).get(
            "confirm_send",
            "⚡ Отправка в Матрицу..."
        )
        await message.answer(confirm_text)

        # Случайный ответ от Матрицы
        responses = TEXTS.get("complete", {}).get(
            "matrix_responses",
            ["✨ Сигнал принят!"]
        )
        matrix_response = random.choice(responses)

        result_suffix = TEXTS.get("complete", {}).get(
            "result_suffix",
            ""
        )

        await message.answer(
            f"{matrix_response}{result_suffix}",
            parse_mode=PARSE_MODE_HTML
        )

        await state.clear()
        logger.info(
            f"Пользователь {message.from_user.id} "
            f"отправил послание в Матрицу"
        )

    except Exception as e:
        logger.error(f"Ошибка в process_matrix_message: {e}")
        await message.answer(ERROR_GENERIC)
        await state.clear()
