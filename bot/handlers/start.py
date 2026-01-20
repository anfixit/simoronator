"""
Обработчик команды /start - Главное меню бота.

Приветствие и навигация по ритуалам.
"""
import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from constants import (
    BTN_ABOUT_SIMORON,
    BTN_GENERATOR_CLIENTS,
    BTN_MAGIC_CODE,
    BTN_MATRIX_MESSAGE,
    PARSE_MODE_HTML,
    WELCOME_TEXT,
)

router = Router()
logger = logging.getLogger(__name__)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Создание клавиатуры главного меню.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с основными ритуалами
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_MAGIC_CODE)],
            [KeyboardButton(text=BTN_GENERATOR_CLIENTS)],
            [KeyboardButton(text=BTN_MATRIX_MESSAGE)],
            [KeyboardButton(text=BTN_ABOUT_SIMORON)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери ритуал..."
    )
    return keyboard


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обработчик команды /start.

    Args:
        message: Сообщение от пользователя
    """
    try:
        keyboard = get_main_menu_keyboard()

        await message.answer(
            WELCOME_TEXT,
            reply_markup=keyboard,
            parse_mode=PARSE_MODE_HTML
        )

        logger.info(
            f"Пользователь {message.from_user.id} "
            f"запустил бота"
        )

    except Exception as e:
        logger.error(f"Ошибка в cmd_start: {e}")


@router.message(F.text == BTN_MAGIC_CODE)
async def show_magic_code(message: Message) -> None:
    """
    Показать меню Волшебного калькулятора.

    Args:
        message: Сообщение от пользователя
    """
    # Перенаправляем на /magic_code
    message.text = "/magic_code"
    from handlers.magic_code import magic_code_menu
    await magic_code_menu(message)


@router.message(F.text == BTN_GENERATOR_CLIENTS)
async def show_generator_clients(message: Message) -> None:
    """
    Показать меню Генератора клиентов.

    Args:
        message: Сообщение от пользователя
    """
    # Перенаправляем на /generator_clients
    message.text = "/generator_clients"
    from handlers.generator_clients import generator_clients_menu
    await generator_clients_menu(message)


@router.message(F.text == BTN_MATRIX_MESSAGE)
async def show_matrix_message(message: Message) -> None:
    """
    Показать меню Matrix Message.

    Args:
        message: Сообщение от пользователя
    """
    # Перенаправляем на /matrix_message
    message.text = "/matrix_message"
    from handlers.matrix_message import matrix_message_menu
    await matrix_message_menu(message)


@router.message(F.text == BTN_ABOUT_SIMORON)
async def show_about(message: Message) -> None:
    """
    Показать информацию о Симороне.

    Args:
        message: Сообщение от пользователя
    """
    try:
        about_text = """
📚 <b>О Симороне</b>

<b>Симорон</b> — это игровая система исполнения желаний,
основанная на лёгкости, юморе и удовольствии от процесса.

🎯 <b>Главные принципы:</b>
• Лёгкость вместо серьёзности
• Игра вместо напряжения
• Удовольствие вместо усилий
• Доверие процессу

✨ <b>Как это работает:</b>
Ритуалы Симорона работают через:
• Переключение фокуса внимания
• Снятие внутренних блоков
• Активацию творческого мышления
• Настройку на позитивное восприятие

🔮 <b>Важно помнить:</b>
Симорон — это не магия в классическом смысле.
Это инструмент работы с собственным подсознанием
через игровые механики и символические действия.

<i>Главное — получать удовольствие от процесса!</i>
"""

        await message.answer(
            about_text,
            parse_mode=PARSE_MODE_HTML
        )

        logger.info(
            f"Пользователь {message.from_user.id} "
            f"запросил информацию о Симороне"
        )

    except Exception as e:
        logger.error(f"Ошибка в show_about: {e}")
