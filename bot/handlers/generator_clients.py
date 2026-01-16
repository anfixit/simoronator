"""
Обработчик команды /generator_clients - Генератор клиентов.

Открывает PWA приложение для ритуала притяжения клиентов.
"""
import logging

from aiogram import F, Router
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from config import Config
from constants import (
    BTN_OPEN_GENERATOR,
    ERROR_WEBAPP,
    MSG_WEBAPP_READY,
    WEBAPP_PATHS,
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "/generator_clients")
async def open_generator_clients(
    message: Message,
    config: Config
) -> None:
    """
    Открытие PWA приложения Генератор клиентов.

    Args:
        message: Сообщение от пользователя
        config: Объект конфигурации приложения
    """
    try:
        # Полный URL с путём к приложению
        webapp_url = (
            f"{config.webapp.base_url}"
            f"{WEBAPP_PATHS['generator_clients']}"
        )

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text=BTN_OPEN_GENERATOR,
                        web_app=WebAppInfo(url=webapp_url)
                    )
                ]
            ],
            resize_keyboard=True
        )

        await message.answer(
            MSG_WEBAPP_READY,
            reply_markup=keyboard
        )

        logger.info(
            f"Пользователь {message.from_user.id} "
            f"открыл generator_clients: {webapp_url}"
        )

    except Exception as e:
        logger.error(f"Ошибка в open_generator_clients: {e}")
        await message.answer(ERROR_WEBAPP)
