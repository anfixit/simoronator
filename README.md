# 🤖 Симоронатор — Телеграм-бот для магических ритуалов

**Симоронатор** — это магический Телеграм-бот, воплощающий симоронские техники и игровой подход к исполнению желаний.
Бот создан на основе старых .exe и .swf программ и воссоздает магические ритуалы в цифровой форме.

---

## ✨ Возможности

Симоронатор умеет:

* Отправлять приказы в Матрицу (`/matrix`)
* Обменивать негатив на полезные ресурсы (`/exchange`)
* Телепортировать тебя в альтернативные миры (`/teleport`)
* Активировать денежную погремушку (`/pogremushka`)
* Заколачивать богатство в доску (`/kolotitel`)
* Подписывать договор с Небесной канцелярией (`/contract`)
* Шифровать мантры в числа (`/encrypt`)
* Генерировать пророчества, сигналы и ритуалы дня (`/random`)

---

## 📆 Установка

> Требуется **Python 3.10+**

1. Клонируй репозиторий:

```bash
git clone https://github.com/anfixit/simoronator.git
cd simoronator
```

2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Создай `.env` файл с токеном бота:

```bash
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

4. Запусти:

```bash
python main.py
```

---

## 📁 Структура проекта

```
simoronator/
├── handlers/        # Файлы с командами и ритуалами
├── keyboards/       # Inline- и reply-кнопки
├── texts/           # Шаблоны текстов и заклинаний
├── data/            # Файлы JSON/хранилища ритуалов
├── utils/           # Утилиты, помощники
├── config.py        # Настройки и константы
├── main.py          # Точка входа
└── README.md        # То, что ты читаешь :)
```

---

## 🧙‍♀️ Автор

Автор: Анфиса Ковганюк
Telegram: [@Anfikus](https://t.me/Anfikus)
GitHub: [anfixit](https://github.com/anfixit)

Проект открыт, вы можете принять участие в развитии, если верите в волшебство и любите Python.
