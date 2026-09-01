# Деплой бота на Google Cloud Run

Бот работает **24/7** без твоего компьютера: Telegram → webhook → Cloud Run, backend → `/v1/notify/*`, связки учеников → **Firestore** (`bot_bindings`).

## Что уже подготовлено в коде

- `Dockerfile` — образ для Cloud Run
- `BOT_MODE=webhook` — вместо polling
- `BINDING_STORE=firestore` — вместо SQLite
- `GET /health` — проверка живости

## Предварительно

1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`)
2. Проект Firebase: **tutorassis** (или свой)
3. Включить API: Cloud Run, Cloud Build, Artifact Registry, Firestore

```powershell
gcloud auth login
gcloud config set project tutorassis
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

## Шаг 1 — секреты

Сгенерируй два случайных ключа (если ещё нет):

```powershell
# BOT_API_SECRET — тот же, что в backend
# WEBHOOK_SECRET — новый, только для Telegram webhook
```

Создай секреты в Secret Manager:

```powershell
echo -n "YOUR_TELEGRAM_BOT_TOKEN" | gcloud secrets create TELEGRAM_BOT_TOKEN --data-file=-
echo -n "YOUR_BOT_API_SECRET" | gcloud secrets create BOT_API_SECRET --data-file=-
echo -n "YOUR_WEBHOOK_SECRET" | gcloud secrets create WEBHOOK_SECRET --data-file=-
```

Если секрет уже есть — добавь новую версию:

```powershell
echo -n "VALUE" | gcloud secrets versions add TELEGRAM_BOT_TOKEN --data-file=-
```

## Шаг 2 — первый деплой

Из папки `bot/`:

```powershell
cd bot
gcloud run deploy simple4u-bot `
  --source . `
  --region europe-west4 `
  --allow-unauthenticated `
  --memory 512Mi `
  --cpu 1 `
  --min-instances 0 `
  --max-instances 3 `
  --set-secrets "TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN:latest,BOT_API_SECRET=BOT_API_SECRET:latest,WEBHOOK_SECRET=WEBHOOK_SECRET:latest" `
  --set-env-vars "BOT_MODE=webhook,BINDING_STORE=firestore,BOT_USERNAME=simp1e4ubot,PUBLIC_SITE_URL=https://simple4u.at,BACKEND_URL=https://tutor-app-backend--tutorassis.europe-west4.hosted.app,WEBHOOK_PATH=/telegram/webhook,GCP_PROJECT=tutorassis"
```

После деплоя скопируй URL сервиса, например:

`https://simple4u-bot-xxxxx.europe-west4.run.app`

## Шаг 3 — webhook URL

Обнови сервис с `WEBHOOK_BASE_URL` (без слэша в конце):

```powershell
gcloud run services update simple4u-bot `
  --region europe-west4 `
  --update-env-vars "WEBHOOK_BASE_URL=https://simple4u-bot-xxxxx.europe-west4.run.app"
```

При старте бот сам вызовет `setWebhook` в Telegram.

Проверка:

```powershell
curl https://simple4u-bot-xxxxx.europe-west4.run.app/health
# {"status":"ok","mode":"webhook"}
```

## Шаг 4 — backend (прод)

В **App Hosting backend** (`tutor-app-backend`) добавь переменные:

| Переменная | Значение |
|---|---|
| `BOT_API_URL` | `https://simple4u-bot-xxxxx.europe-west4.run.app` |
| `BOT_API_SECRET` | тот же, что `BOT_API_SECRET` |
| `BOT_USERNAME` | `simp1e4ubot` |

Передеплой backend после изменения env.

## Шаг 5 — проверка

1. В CRM открой ученика с Telegram → ссылка должна регистрироваться (`POST /v1/links`)
2. Ученик жмёт `/start <token>` в боте
3. Сделай тестовое пополнение → push в Telegram
4. Меню бота: Занятия / Оплата / Главная

## Локальная разработка (как раньше)

```powershell
cd bot
.\.venv\Scripts\Activate.ps1
copy .env.example .env
# BOT_MODE=polling, BINDING_STORE=sqlite
pip install -e ".[dev]"
simple4u-bot
```

## Повторный деплой после изменений

```powershell
cd bot
gcloud run deploy simple4u-bot --source . --region europe-west4
```

## Миграция с SQLite

Firestore начинает пустым. Связки `student_id ↔ token` создаются, когда backend вызывает `/v1/links` (при открытии карточки ученика / включении бота).

**Ученикам, уже подключённым локально:** один раз снова открыть ссылку `/start` в Telegram.

## Стоимость

Cloud Run: оплата за запросы + немного за память. При webhook и `min-instances=0` обычно **$0–5/мес** на небольшой трафик.

## Проблемы

| Симптом | Решение |
|---|---|
| Бот не отвечает | Проверь `WEBHOOK_BASE_URL`, логи: `gcloud run services logs read simple4u-bot --region europe-west4` |
| 401 на notify | `BOT_API_SECRET` не совпадает между backend и ботом |
| Уведомления не идут | `BOT_API_URL` в backend указывает на Cloud Run URL |
| Firestore permission denied | Сервисный аккаунт Cloud Run нужен `roles/datastore.user` |
