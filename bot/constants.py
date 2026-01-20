"""Константы приложения."""
from pathlib import Path
from typing import Final

# Пути
BOT_DIR: Final[Path] = Path(__file__).parent
TEXTS_DIR: Final[Path] = BOT_DIR / "texts"
HELP_DIR: Final[Path] = BOT_DIR / "help"

# Пути к PWA приложениям
WEBAPP_PATHS: Final[dict[str, str]] = {
    "magic_code": "/magic_code/",
    "generator_clients": "/generator_clients/",
    "matrix_message": "/MatrixMessage/",
}

# Сообщения об ошибках
ERROR_GENERIC: Final[str] = (
    "⚠️ Произошла ошибка. Попробуй позже."
)
ERROR_WEBAPP: Final[str] = (
    "⚠️ Произошла ошибка при открытии приложения. "
    "Попробуй позже."
)
ERROR_HELP_UNAVAILABLE: Final[str] = "❗ Справка пока недоступна."

# Magic Code
MIN_FIO_WORDS: Final[int] = 4
MAGIC_CODE_COMPRESS_LIMIT: Final[int] = 999

# Алфавит для кодирования
RU_ALPHABET: Final[str] = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# Regex паттерны
PATTERN_NON_RU_DIGIT: Final[str] = r"[^А-Яа-я0-9]"

# Parse mode
PARSE_MODE_HTML: Final[str] = "HTML"
PARSE_MODE_MARKDOWN: Final[str] = "Markdown"

# Тексты кнопок
BTN_OPEN_GENERATOR: Final[str] = "🧲 Открыть генератор"
BTN_OPEN_MAGIC_CODE: Final[str] = "🔮 Открыть калькулятор"
BTN_OPEN_MATRIX: Final[str] = "📡 Открыть связь с Матрицей"

# Приветственные сообщения для WebApp
MSG_WEBAPP_READY: Final[str] = (
    "✨ Готово! Нажми кнопку ниже, чтобы запустить:"
)
