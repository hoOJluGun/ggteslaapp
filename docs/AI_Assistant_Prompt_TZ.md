# Техническое задание (ТЗ) для AI-Ассистента

**Контекст проекта:**
Мы разрабатываем "GG Tesla App Platform" — Event-Driven Monorepo (Node.js/Fastify, React/Vite, Rust, Telegram Bot) с использованием шины событий NATS. Инфраструктура, Docker Compose, CI/CD Pipeline (GitHub Actions) и Helm Chart уже настроены.

Но сейчас нам нужно "мясо" — реальный рабочий код микросервисов. 

**Твоя задача:**
Напиши код для 3-х ключевых модулей платформы. Предоставь полный код для каждого из указанных файлов. Не ломай существующую логику, используй TypeScript (TS) и Rust.

---

### ЗАДАЧА 1: Реализовать Backend Core (Node.js + Fastify)
**Файл:** `core/helio/src/index.ts`
Что нужно сделать:
1. Инициализировать Fastify сервер (на порту 3000, host: '0.0.0.0').
2. Добавить плагины `@fastify/swagger` и `@fastify/swagger-ui` (OpenAPI v3.0).
3. При старте сервера подключаться к NATS JetStream (URL из `process.env.NATS_URL`). Если NATS недоступен, не ронять сервер (graceful fallback).
4. Создать `POST /events/:subject`. Этот эндпоинт должен валидировать входящий JSON-payload через Fastify JSON Schema validator, и если всё ок, публиковать событие в NATS-топик, переданный в URL.
5. Создать `GET /health` возвращающий `{"status": "OK", "nats_connected": true/false}`.

---

### ЗАДАЧА 2: Реализовать Telegram-бота (Node.js + TS)
**Файл:** `apps/telegram-bot/src/index.ts`
Что нужно сделать:
1. Использовать `node-telegram-bot-api`. Токен брать из `process.env.TELEGRAM_BOT_TOKEN`.
2. Подключиться к NATS (`process.env.NATS_URL`).
3. Команды, которые бот должен поддерживать и логировать в NATS:
   - `/start` — Приветственное сообщение Markdown: "Добро пожаловать в платформу GG Tesla!". Публикует событие `telegram.bot.start` в NATS.
   - `/help` — Справка по командам.
   - `/status` — Отправляет HTTP GET запрос на `helio-core:3000/health` (внутри Docker сети) и возвращает статус.
   - `/role <role>` — Сохраняет роль (in-memory) и публикует событие `authz.role.assign.v1` в NATS с Payload'ом: `{ "userId": chat_id, "role": "<role>" }`.

---

### ЗАДАЧА 3: Реализовать стартовый UI на React
**Файл:** `apps/web/src/App.tsx`
Что нужно сделать:
1. Использовать `react-router-dom` и `react-query` и `zustand` (они уже есть в `package.json`).
2. Создать Zustand-store для хранения стейта: `role` (строка), `notifications` (массив).
3. Создать страницу Dashboard, которая содержит большую кнопку «Ping API».
4. По клику на кнопку `react-query` должен отправлять POST-запрос на `http://localhost:3000/events/web.action.trigger` (отправляем на helio-core).
5. Нарисовать красивый PWA интерфейс с применением современного CSS (любой стиль, без Tailwind, обычный CSS. Темная тема).

---

**Требования к ответу Ассистента:**
- Выдавай только валидный код без лишних рассуждений. 
- Обрати внимание, что сервисы крутятся в Docker-сети, поэтому Web-приложение должно стучаться на localhost (или кастомный хост, прокинутый через proxy), а Telegram-бот будет стучаться на `http://helio-core:3000`.
