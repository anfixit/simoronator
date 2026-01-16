"""
Модуль для кодирования текста в магические числовые коды.

Преобразует русский текст и цифры в числовой код на основе
позиций букв в алфавите с опциональным сжатием до 3 цифр.
"""
import re
from typing import Final

from constants import (
    MAGIC_CODE_COMPRESS_LIMIT,
    PATTERN_NON_RU_DIGIT,
    RU_ALPHABET,
)

# Русский алфавит с номерами: А=1, Б=2, ..., Я=33
ALPHABET: Final[dict[str, int]] = {
    letter: idx
    for idx, letter in enumerate(RU_ALPHABET, start=1)
}


def encode_magic_code(text: str, compress: bool = True) -> str:
    """
    Преобразует текст в числовой магический код.

    Принцип работы:
    - Каждая русская буква заменяется на её номер в алфавите
    - Цифры остаются без изменений
    - Пробелы и спецсимволы игнорируются
    - Если compress=True, код сжимается до ≤999

    Args:
        text: Входной текст для кодирования
        compress: Сжать ли результат до трёхзначного числа

    Returns:
        Строка с числовым кодом

    Example:
        >>> encode_magic_code("Привет", compress=False)
        '16181015320'
        >>> encode_magic_code("Привет", compress=True)
        '23'
    """
    cleaned: str = re.sub(
        PATTERN_NON_RU_DIGIT,
        "",
        text.upper()
    )
    code_digits: list[str] = []

    for char in cleaned:
        if char.isdigit():
            code_digits.append(char)
        elif char in ALPHABET:
            code_digits.append(str(ALPHABET[char]))

    full_code: str = "".join(code_digits)

    if not compress:
        return full_code

    # Сжатие: сумма цифр, пока не станет ≤999
    result: int = sum(int(d) for d in full_code)

    while result > MAGIC_CODE_COMPRESS_LIMIT:
        result = sum(int(d) for d in str(result))

    return str(result)
