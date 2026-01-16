"""Конфигурация телеграм-бота Симоронатор."""
from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class BotConfig:
    """Конфигурация телеграм-бота."""

    token: str
    admin_ids: list[int]


@dataclass
class WebAppConfig:
    """Конфигурация PWA приложений."""

    base_url: str


@dataclass
class Config:
    """Главная конфигурация приложения."""

    bot: BotConfig
    webapp: WebAppConfig


def load_config(path: Optional[str] = None) -> Config:
    """
    Загрузка конфигурации из .env файла.

    Args:
        path: Путь к .env файлу. Если None, ищет в текущей директории.

    Returns:
        Config: Объект конфигурации со всеми настройками.

    Raises:
        EnvError: Если обязательные переменные окружения не найдены.
    """
    env = Env()
    env.read_env(path)

    return Config(
        bot=BotConfig(
            token=env.str("BOT_TOKEN"),
            admin_ids=env.list("ADMIN_IDS", subcast=int, default=[]),
        ),
        webapp=WebAppConfig(
            base_url=env.str(
                "WEBAPP_URL",
                default="https://simoronator.ru"
            ),
        ),
    )
