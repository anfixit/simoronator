document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("client-form");
  const zone = document.getElementById("generation-zone");
  const log = document.getElementById("clients-log");

  const clients = [
    "📞 Звонок от потенциального клиента...",
    "💬 Кто-то интересуется вашим продуктом...",
    "📩 Новое письмо с заявкой!",
    "🚀 Входящий лид направлен к вам...",
    "👥 Заказчик просит презентацию!",
    "🎯 Попадание в целевую аудиторию!",
    "📲 Телеграм-чат оживился...",
    "💼 Приходит корпоративный клиент...",
    "🧾 Запрос на расчёт стоимости.",
    "📎 Отклик с вашей формы обратной связи..."
  ];

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    // Скрываем форму и запускаем генерацию
    form.classList.add("hidden");
    zone.classList.remove("hidden");

    log.innerHTML = ""; // очищаем лог

    let i = 0;

    const interval = setInterval(() => {
      const msg = document.createElement("div");
      msg.textContent = clients[i % clients.length];
      log.appendChild(msg);
      log.scrollTop = log.scrollHeight;

      i++;

      // Останавливаем через 10 сообщений
      if (i === 10) {
        clearInterval(interval);
        const done = document.createElement("div");
        done.innerHTML = "<br>✅ Поток клиентов направлен!";
        done.style.color = "#2ee5ab";
        log.appendChild(done);
      }
    }, 800);
  });
});
