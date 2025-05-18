import re

# Простой алфавитный кодировщик: А=1, Б=2, ..., Я=33
ALPHABET = {
    letter: idx for idx, letter in enumerate(
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', start=1
    )
}

def encode_magic_code(text: str) -> str:
    """
    Преобразует текст в числовой код по принципу:
    - Каждая русская буква заменяется на её номер в алфавите
    - Цифры остаются как есть
    - Пробелы и символы игнорируются
    """
    cleaned = re.sub(r"[^А-Яа-я0-9]", "", text.upper())
    code_digits = []

    for char in cleaned:
        if char.isdigit():
            code_digits.append(char)
        elif char in ALPHABET:
            code_digits.append(str(ALPHABET[char]))

    return ''.join(code_digits)
