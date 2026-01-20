"""
Главный модуль телеграм-бота Симоронатор.

Инициализация бота, регистрация handlers, запуск polling.
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config
from handlers import (
    generator_clients,
    magic_code,
    matrix_message,
    start,
)
from handlers import (
    help as help_handler,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            "bot.log",
            encoding="utf-8"
        )
    ]
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Главная функция запуска бота.

    Инициализирует бот, регистрирует handlers и запускает polling.
    """
    try:
        # Загрузка конфигурации
        config = load_config()
        logger.info("Конфигурация загружена успешно")

        # Инициализация бота и диспетчера
        bot = Bot(
            token=config.bot.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Регистрация роутеров
        dp.include_router(start.router)
        dp.include_router(magic_code.router)
        dp.include_router(generator_clients.router)
        dp.include_router(matrix_message.router)
        dp.include_router(help_handler.router)

        logger.info("Роутеры зарегистрированы")

        # Передача config в middleware
        dp["config"] = config

        # Удаление вебхука и запуск polling
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот запущен и готов к работе!")

        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.critical(f"Неожиданная ошибка: {e}")
        sys.exit(1)
