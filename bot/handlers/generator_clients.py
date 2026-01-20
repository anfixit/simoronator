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
    BTN_BEAUTIFUL_VERSION,
    BTN_HOW_IT_WORKS,
    BTN_OPEN_GENERATOR,
    BTN_TO_MAIN_MENU,
    ERROR_WEBAPP,
    MSG_WEBAPP_READY,
    PARSE_MODE_HTML,
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
                        text=BTN_BEAUTIFUL_VERSION,
                        callback_data="generator_clients_pwa"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=BTN_HOW_IT_WORKS,
                        callback_data="help_generator_clients"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=BTN_TO_MAIN_MENU,
                        callback_data="main_menu"
                    )
                ]
            ]
        )

        await message.answer(
            "🧲 <b>Генератор клиентов</b>\n\n"
            "Визуальный ритуал притяжения клиентов.\n"
            "Доступен только в красивой версии:",
            reply_markup=keyboard,
            parse_mode=PARSE_MODE_HTML
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


@router.callback_query(F.data == "help_generator_clients")
async def show_help_generator_clients(callback) -> None:
    """
    Показать справку по Генератору клиентов.

    Args:
        callback: Callback query
    """
    try:
        from handlers.help import read_help

        text = read_help("generator_clients")
        if text:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="← Назад",
                            callback_data="back_to_generator_clients"
                        )
                    ]
                ]
            )
            await callback.message.edit_text(
                text,
                parse_mode=PARSE_MODE_HTML,
                reply_markup=keyboard
            )
        else:
            await callback.message.edit_text(
                "❗ Справка временно недоступна."
            )

        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка в show_help_generator_clients: {e}")
        await callback.answer("Ошибка загрузки справки")


@router.callback_query(F.data == "back_to_generator_clients")
async def back_to_generator_clients_menu(
    callback,
    message: Message = None
) -> None:
    """
    Возврат в меню generator_clients.

    Args:
        callback: Callback query
        message: Message (опционально)
    """
    msg = message or callback.message
    msg.text = "/generator_clients"
    await generator_clients_menu(msg)
    if callback:
        await callback.answer()


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback) -> None:
    """
    Возврат в главное меню.

    Args:
        callback: Callback query
    """
    try:
        from constants import WELCOME_TEXT

        from handlers.start import get_main_menu_keyboard

        keyboard = get_main_menu_keyboard()

        await callback.message.delete()
        await callback.message.answer(
            WELCOME_TEXT,
            reply_markup=keyboard,
            parse_mode=PARSE_MODE_HTML
        )

        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка в back_to_main_menu: {e}")
        await callback.answer("Ошибка возврата в меню")
