# Simple4U Bot (Python)

Отдельный подрепозиторий Telegram-бота для учеников. Сообщения совпадают с превью на landing-v2:

| Событие | Пример |
|---------|--------|
| Баланс | Привет! В пакете осталось 2 занятия. |
| Оплата | Оплата получена: €225 · +5 занятий. Спасибо! |
| Старт урока | Через 30 минут начинается урок · 11:30 |
| Домашка | Домашка на сегодня: упр. 4–6, стр. 18. |
| Перенос | Урок перенесён. Новое время: … |

Ученик включает уведомления в CRM (`bot_active`); привязка чата — deep link `/start <token>`.

## Стек

- Python 3.11+
- [aiogram](https://docs.aiogram.dev/) 3 — polling Telegram
- FastAPI — HTTP API для вызовов из Express backend
- SQLite — локальные связки `student_id ↔ chat_id` (MVP)

## Быстрый старт

```bash
cd bot
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -e ".[dev]"
copy .env.example .env   # или cp .env.example .env
# Заполни TELEGRAM_BOT_TOKEN и BOT_API_SECRET
simple4u-bot
```

HTTP по умолчанию: `http://127.0.0.1:8081`.

## HTTP API (секрет в заголовке `X-Bot-Secret`)

### Зарегистрировать ссылку ученика

```http
POST /v1/links
X-Bot-Secret: <BOT_API_SECRET>
Content-Type: application/json

{
  "student_id": "stu_abc",
  "link_token": "opaque-random-token",
  "student_name": "Anna",
  "bot_active": true
}
```

Ответ содержит `deep_link`: `https://t.me/<BOT_USERNAME>?start=<token>`.

### Уведомления

```http
POST /v1/notify/balance
POST /v1/notify/payment
POST /v1/notify/lesson-start
POST /v1/notify/homework
POST /v1/notify/lesson-moved
POST /v1/bot-active
```

Примеры тел:

```json
{ "student_id": "stu_abc", "lessons_left": 2 }
{ "student_id": "stu_abc", "amount_label": "€225", "lessons_added": 5 }
{ "student_id": "stu_abc", "minutes_before": 30, "time_label": "11:30" }
{ "student_id": "stu_abc", "text": "упр. 4–6, стр. 18." }
{ "student_id": "stu_abc", "new_time_label": "Чт · 15:00" }
{ "student_id": "stu_abc", "bot_active": false }
```

`GET /health` — без секрета.

## Команды в Telegram

- `/start <token>` — привязать чат
- `/status` — проверить связку

## Тесты

```bash
pytest
```

## Git

Это **отдельный git-репозиторий** внутри `tutor-app/bot` (как `backend/`).  
Remote на GitHub завести отдельно, когда будете готовы (например `wrincied/tutor-app-bot`).

## Дальше (интеграция)

1. Express backend: при оплате / переносе / напоминании → `POST /v1/notify/...`
2. CRM: генерация `link_token` + показ deep link ученику
3. Деплой: контейнер / App Hosting / отдельный VPS с `TELEGRAM_BOT_TOKEN`
