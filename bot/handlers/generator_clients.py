"""
Обработчик команды /generator_clients - Генератор клиентов.

Открывает PWA приложение для ритуала притяжения клиентов.
"""
import logging

from aiogram import F, Router
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
    BTN_OPEN_GENERATOR,
    ERROR_WEBAPP,
    MSG_WEBAPP_READY,
    WEBAPP_PATHS,
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "/generator_clients")
async def generator_clients_menu(message: Message) -> None:
    """
    Меню выбора режима работы генератора.

    Args:
        message: Сообщение от пользователя
    """
    try:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✨ Красивая версия (PWA)",
                        callback_data="generator_clients_pwa"
                    )
                ]
            ]
        )

        await message.answer(
            "🧲 <b>Генератор клиентов</b>\n\n"
            "Визуальный ритуал притяжения клиентов.\n"
            "Доступен только в PWA версии:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

        logger.info(
            f"Пользователь {message.from_user.id} "
            f"открыл меню generator_clients"
        )

    except Exception as e:
        logger.error(f"Ошибка в generator_clients_menu: {e}")
        await message.answer(ERROR_WEBAPP)


@router.callback_query(F.data == "generator_clients_pwa")
async def open_generator_clients(
    callback,
    config: Config
) -> None:
    """
    Открытие PWA приложения Генератор клиентов.

    Args:
        callback: Callback query
        config: Объект конфигурации приложения
    """
    try:
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

        await callback.message.edit_text(MSG_WEBAPP_READY)
        await callback.message.answer(
            "Нажми кнопку ниже:",
            reply_markup=keyboard
        )

        await callback.answer()

        logger.info(
            f"Пользователь {callback.from_user.id} "
            f"открыл generator_clients: {webapp_url}"
        )

    except Exception as e:
        logger.error(f"Ошибка в open_generator_clients: {e}")
        await callback.message.answer(ERROR_WEBAPP)
        await callback.answer()
