/**
 * Волшебный калькулятор Симорон - PWA приложение.
 *
 * Генерирует персональный магический код из намерения
 * и личных данных пользователя.
 */

// Константы конфигурации
const CONFIG = {
  MIN_FIELD_LENGTH: 1,
  COMPRESS_LIMIT: 999,
};

// Константы сообщений
const MESSAGES = {
  EMPTY_FIELDS: "Заполни оба поля, пожалуйста.",
  RU_ALPHABET: "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
};

// Regex паттерны
const PATTERNS = {
  NON_RU_DIGIT: /[^А-Я0-9]/g,
  DIGIT: /[0-9]/,
};

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("magic-form");
  const resultBlock = document.getElementById("result");
  const codeOutput = document.getElementById("code-output");

  form.addEventListener("submit", handleFormSubmit);

  /**
   * Обработчик отправки формы.
   *
   * @param {Event} e - Event объект
   */
  function handleFormSubmit(e) {
    e.preventDefault();

    const intent = document.getElementById("intent").value.trim();
    const identity = document.getElementById("identity").value.trim();

    if (!intent || !identity) {
      alert(MESSAGES.EMPTY_FIELDS);
      return;
    }

    const fullText = `${intent} ${identity}`;
    const code = generateMagicCode(fullText);

    codeOutput.textContent = code;
    resultBlock.classList.remove("hidden");
  }

  /**
   * Генерирует магический код из текста.
   *
   * @param {string} text - Входной текст
   * @returns {string} Трёхзначный магический код
   */
  function generateMagicCode(text) {
    const clean = text.toUpperCase().replace(PATTERNS.NON_RU_DIGIT, "");

    let numericString = "";
    for (let char of clean) {
      if (PATTERNS.DIGIT.test(char)) {
        numericString += char;
      } else {
        const index = MESSAGES.RU_ALPHABET.indexOf(char);
        if (index !== -1) {
          numericString += (index + 1).toString();
        }
      }
    }

    return compressToThreeDigits(numericString);
  }

  /**
   * Сжимает числовую строку до трёхзначного числа.
   *
   * @param {string} numericString - Числовая строка
   * @returns {string} Сжатое число (≤999)
   */
  function compressToThreeDigits(numericString) {
    let sum = numericString.split("").reduce((a, b) => a + Number(b), 0);

    while (sum > CONFIG.COMPRESS_LIMIT) {
      sum = sum
        .toString()
        .split("")
        .reduce((a, b) => a + Number(b), 0);
    }

    return sum.toString();
  }
});
