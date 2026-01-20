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
    BTN_OPEN_MAGIC_CODE,
    BTN_QUICK_IN_BOT,
    BTN_TO_MAIN_MENU,
    ERROR_GENERIC,
    ERROR_WEBAPP,
    MIN_FIO_WORDS,
    MSG_WEBAPP_READY,
    PARSE_MODE_HTML,
    PARSE_MODE_MARKDOWN,
    TEXTS_DIR,
    WEBAPP_PATHS,
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


@router.message(F.text == "/magic_code")
async def magic_code_menu(message: Message) -> None:
    """
    Меню выбора режима работы калькулятора.

    Args:
        message: Сообщение от пользователя
    """
    try:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=BTN_BEAUTIFUL_VERSION,
                        callback_data="magic_code_pwa"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=BTN_QUICK_IN_BOT,
                        callback_data="magic_code_bot"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=BTN_HOW_IT_WORKS,
                        callback_data="help_magic_code"
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
            "🔮 <b>Волшебный калькулятор</b>\n\n"
            "Генерация персонального магического кода "
            "из твоего намерения.\n\n"
            "Выбери способ запуска:",
            reply_markup=keyboard,
            parse_mode=PARSE_MODE_HTML
        )

        logger.info(
            f"Пользователь {message.from_user.id} "
            f"открыл меню magic_code"
        )

    except Exception as e:
        logger.error(f"Ошибка в magic_code_menu: {e}")
        await message.answer(ERROR_GENERIC)


@router.callback_query(F.data == "magic_code_pwa")
async def open_magic_code_pwa(
    callback,
    config: Config
) -> None:
    """
    Открытие PWA приложения Волшебный калькулятор.

    Args:
        callback: Callback query
        config: Объект конфигурации приложения
    """
    try:
        webapp_url = (
            f"{config.webapp.base_url}"
            f"{WEBAPP_PATHS['magic_code']}"
        )

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text=BTN_OPEN_MAGIC_CODE,
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
            f"открыл magic_code PWA: {webapp_url}"
        )

    except Exception as e:
        logger.error(f"Ошибка в open_magic_code_pwa: {e}")
        await callback.message.answer(ERROR_WEBAPP)
        await callback.answer()


@router.callback_query(F.data == "magic_code_bot")
async def start_magic_code_bot(
    callback,
    state: FSMContext
) -> None:
    """
    Начало ритуала генерации магического кода в боте.

    Args:
        callback: Callback query
        state: Контекст состояния FSM
    """
    try:
        text = TEXTS.get("start", {}).get(
            "ask_intent",
            "🔮 Напиши своё намерение."
        )

        await callback.message.edit_text(text)
        await state.set_state(MagicCodeStates.waiting_for_intent)
        await callback.answer()

        logger.info(
            f"Пользователь {callback.from_user.id} "
            f"начал ритуал magic_code в боте"
        )

    except Exception as e:
        logger.error(f"Ошибка в start_magic_code_bot: {e}")
        await callback.message.answer(ERROR_GENERIC)
        await callback.answer()


@router.callback_query(F.data == "help_magic_code")
async def show_help_magic_code(callback) -> None:
    """
    Показать справку по Волшебному калькулятору.

    Args:
        callback: Callback query
    """
    try:
        from handlers.help import read_help

        text = read_help("magic_code")
        if text:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="← Назад",
                            callback_data="back_to_magic_code"
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
        logger.error(f"Ошибка в show_help_magic_code: {e}")
        await callback.answer("Ошибка загрузки справки")


@router.callback_query(F.data == "back_to_magic_code")
async def back_to_magic_code_menu(callback, message: Message = None) -> None:
    """
    Возврат в меню magic_code.

    Args:
        callback: Callback query
        message: Message (опционально)
    """
    msg = message or callback.message
    msg.text = "/magic_code"
    await magic_code_menu(msg)
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
        from handlers.start import get_main_menu_keyboard
        from constants import WELCOME_TEXT

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
