/**
 * Генератор клиентов - PWA приложение.
 *
 * Визуализирует ритуал притяжения клиентов через анимацию
 * входящих запросов и сообщений.
 */

// Константы конфигурации
const CONFIG = {
  MAX_LOG_LINES: 5,
  ANIMATION_INTERVAL: 900,
  COMPLETION_DELAY: 1400,
  TOTAL_ITERATIONS: 10,
};

// Сообщения для визуализации потока клиентов
const CLIENT_MESSAGES = [
  "📞 Звонок от потенциального клиента...",
  "💬 Кто-то интересуется вашим продуктом...",
  "📩 Новое письмо с заявкой!",
  "🚀 Входящий лид направлен к вам...",
  "👥 Заказчик просит презентацию!",
  "🎯 Попадание в целевую аудиторию!",
  "📲 Телеграм-чат оживился...",
  "💼 Приходит корпоративный клиент...",
  "🧾 Запрос на расчёт стоимости.",
  "📎 Отклик с вашей формы обратной связи...",
];

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("client-form");
  const zone = document.getElementById("generation-zone");
  const log = document.getElementById("clients-log");

  form.addEventListener("submit", handleFormSubmit);

  /**
   * Обработчик отправки формы.
   *
   * @param {Event} e - Event объект
   */
  function handleFormSubmit(e) {
    e.preventDefault();
    startGeneration();
  }

  /**
   * Запуск визуализации генерации клиентов.
   */
  function startGeneration() {
    form.classList.add("hidden");
    zone.classList.remove("hidden");
    log.innerHTML = "";

    let iteration = 0;
    const interval = setInterval(() => {
      addMessageToLog(iteration);
      iteration++;

      if (iteration === CONFIG.TOTAL_ITERATIONS) {
        clearInterval(interval);
        showCompletionMessages();
      }
    }, CONFIG.ANIMATION_INTERVAL);
  }

  /**
   * Добавляет сообщение в лог визуализации.
   *
   * @param {number} index - Индекс итерации
   */
  function addMessageToLog(index) {
    const msg = document.createElement("div");
    msg.textContent = CLIENT_MESSAGES[index % CLIENT_MESSAGES.length];
    msg.style.opacity = "0";
    msg.style.transition = "opacity 0.5s ease";
    log.appendChild(msg);

    requestAnimationFrame(() => {
      msg.style.opacity = "1";
    });

    limitLogLines();
  }

  /**
   * Ограничивает количество строк в логе.
   */
  function limitLogLines() {
    while (log.children.length > CONFIG.MAX_LOG_LINES) {
      log.removeChild(log.firstChild);
    }
  }

  /**
   * Показывает финальные сообщения о завершении.
   */
  function showCompletionMessages() {
    // Первое сообщение
    setTimeout(() => {
      const msg1 = document.createElement("div");
      msg1.innerHTML =
        "✅ <span style='color: #2ee5ab;'>" +
        "Поток клиентов направлен!</span>";
      msg1.style.marginTop = "1rem";
      msg1.style.opacity = "0";
      msg1.style.transition = "opacity 0.6s ease";
      log.appendChild(msg1);

      requestAnimationFrame(() => {
        msg1.style.opacity = "1";
      });
    }, 0);

    // Второе сообщение
    setTimeout(() => {
      const msg2 = document.createElement("div");
      msg2.innerHTML = "✨ <em>Ждите — поток уже на пути к вам...</em>";
      msg2.style.marginTop = "0.8rem";
      msg2.style.opacity = "0";
      msg2.style.transition = "opacity 0.8s ease";
      log.appendChild(msg2);

      requestAnimationFrame(() => {
        msg2.style.opacity = "1";
      });
    }, CONFIG.COMPLETION_DELAY);
  }
});
