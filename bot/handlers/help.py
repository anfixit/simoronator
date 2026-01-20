"""
Обработчик команд справки.

Предоставляет пользователям информацию о доступных ритуалах.
"""
import logging
import re

from aiogram import F, Router
from aiogram.types import Message
from constants import (
    ERROR_GENERIC,
    ERROR_HELP_UNAVAILABLE,
    HELP_DIR,
)

router = Router()
logger = logging.getLogger(__name__)


def markdown_to_telegram_html(text: str) -> str:
    """
    Конвертирует Markdown в Telegram HTML.

    Args:
        text: Markdown текст

    Returns:
        HTML текст для Telegram
    """
    # Заголовки ## -> <b>
    text = re.sub(r'^## (.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    # Жирный текст **text** -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # Курсив *text* -> <i>text</i>
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)

    # Удалить горизонтальные линии ---
    text = re.sub(r'^---$', '', text, flags=re.MULTILINE)

    # Удалить лишние пустые строки
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def read_help(name: str) -> str | None:
    """
    Чтение файла справки по имени.

    Args:
        name: Имя файла справки без расширения

    Returns:
        Содержимое файла или None при ошибке

    Example:
        >>> read_help("magic_code")
        '# СПРАВКА: Волшебный калькулятор...'
    """
    try:
        path = HELP_DIR / f"{name}.md"
        if path.exists():
            md_text = path.read_text(encoding="utf-8")
            return markdown_to_telegram_html(md_text)
        else:
            logger.warning(f"Файл справки не найден: {path}")
            return None
    except Exception as e:
        logger.error(f"Ошибка чтения справки {name}: {e}")
        return None


@router.message(F.text == "/help_magic_code")
async def help_magic_code(message: Message) -> None:
    """
    Справка по команде /magic_code.

    Args:
        message: Сообщение от пользователя
    """
    try:
        text = read_help("magic_code")
        if text:
            await message.answer(text, parse_mode="HTML")
            logger.info(
                f"Пользователь {message.from_user.id} "
                f"запросил справку magic_code"
            )
        else:
            await message.answer(ERROR_HELP_UNAVAILABLE)
    except Exception as e:
        logger.error(f"Ошибка в help_magic_code: {e}")
        await message.answer(ERROR_GENERIC)


@router.message(F.text == "/help_generator_clients")
async def help_generator_clients(message: Message) -> None:
    """
    Справка по команде /generator_clients.

    Args:
        message: Сообщение от пользователя
    """
    try:
        text = read_help("generator_clients")
        if text:
            await message.answer(text, parse_mode="HTML")
            logger.info(
                f"Пользователь {message.from_user.id} "
                f"запросил справку generator_clients"
            )
        else:
            await message.answer(ERROR_HELP_UNAVAILABLE)
    except Exception as e:
        logger.error(f"Ошибка в help_generator_clients: {e}")
        await message.answer(ERROR_GENERIC)

@router.message(F.text == "/help_matrix_message")
async def help_matrix_message(message: Message) -> None:
    """
    Справка по команде /matrix_message.

    Args:
        message: Сообщение от пользователя
    """
    try:
        text = read_help("matrix_message")
        if text:
            await message.answer(text, parse_mode="HTML")
            logger.info(
                f"Пользователь {message.from_user.id} "
                f"запросил справку matrix_message"
            )
        else:
            await message.answer(ERROR_HELP_UNAVAILABLE)
    except Exception as e:
        logger.error(f"Ошибка в help_matrix_message: {e}")
        await message.answer(ERROR_GENERIC)
