/**
 * Matrix Message - PWA приложение.
 *
 * Отправка магических сообщений в Матрицу реальности
 * с визуальной анимацией.
 */

// Константы конфигурации
const CONFIG = {
  ANIMATION_DURATION: 3000,
  MATRIX_RESPONSES: [
    "✨ Сигнал принят. Матрица активирует события для материализации.",
    "🌠 Послание зарегистрировано в Реестре Возможностей.",
    "⚛️ Квантовые вероятности перестроены в твою пользу.",
    "🔮 Поток направлен. Синхроничности уже на пути.",
    "💫 Твой запрос передан в Центральный Узел Изобилия.",
    "🌀 Матрица пересчитала маршруты. Ожидай знаков.",
    "✅ Подтверждено. Вселенная откликается на частоту твоего намерения.",
    "🎯 Цель зафиксирована. Реальность начинает подстройку.",
    "🌌 Твоё послание отправлено в Архив Исполненных Желаний.",
    "⚡ Энергия намерения усилена. Материализация запущена.",
  ],
};

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("matrix-form");
  const responseDiv = document.getElementById("response");
  const replyDiv = document.getElementById("reply");

  form.addEventListener("submit", handleFormSubmit);

  /**
   * Обработчик отправки формы.
   *
   * @param {Event} e - Event объект
   */
  function handleFormSubmit(e) {
    e.preventDefault();

    const message = document.getElementById("message").value.trim();

    if (!message) {
      alert("Напиши своё послание!");
      return;
    }

    sendToMatrix(message);
  }

  /**
   * Отправка сообщения в Матрицу с анимацией.
   *
   * @param {string} message - Текст послания
   */
  function sendToMatrix(message) {
    form.classList.add("hidden");
    responseDiv.classList.remove("hidden");

    // Анимация отправки
    setTimeout(() => {
      const randomResponse =
        CONFIG.MATRIX_RESPONSES[
          Math.floor(Math.random() * CONFIG.MATRIX_RESPONSES.length)
        ];

      replyDiv.innerHTML = `
        <div style="
          background: rgba(0, 255, 153, 0.1);
          border: 1px solid #00ff99;
          border-radius: 0.5rem;
          padding: 1rem;
          margin-top: 1rem;
          animation: fadeIn 0.8s ease;
        ">
          <p style="margin-bottom: 1rem;">${randomResponse}</p>
          <div style="
            font-size: 0.85rem;
            opacity: 0.8;
            border-top: 1px solid rgba(0, 255, 153, 0.3);
            padding-top: 0.8rem;
            margin-top: 0.8rem;
          ">
            🔔 <b>Рекомендация:</b><br>
            В ближайшие 3 дня обращай внимание на:<br>
            • Случайные встречи<br>
            • Необычные совпадения<br>
            • Внезапные идеи<br>
            • Знаки и символы<br><br>
            Матрица уже работает! ✨
          </div>
        </div>
      `;

      // Скрыть анимацию загрузки
      document.querySelector(".matrix-flux").style.display = "none";
    }, CONFIG.ANIMATION_DURATION);
  }
});
