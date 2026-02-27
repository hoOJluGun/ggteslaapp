# GG Tesla App Platform Scaffold

Каркас production‑ориентированной full‑stack платформы с HELIO core, realtime-шиной событий и cloud-native деплоем.

## Что включено
- Web PWA: React + TypeScript (`apps/web`) + Dockerfile.
- Backend core: Node.js/TypeScript (`core/helio`) + NATS/JetStream.
- Rust микросервисы (`microservices/*`): SFU, CRDT sync, reporting, authz.
- Telegram-бот (`apps/telegram-bot`) на той же event bus.
- Desktop scaffolding: macOS Intel (FastMCP-Rust/CocoaKit stubs) и Windows+NSIS.
- Инфраструктура: NATS, PostgreSQL, Redis, ChromaDB, Vault, Ollama, Scout.
- Деплой: Helm chart + Argo CD app + GitHub Actions CI/CD.
- Политики: Vault + OPA.

## Структура каталогов
```text
.
├── apps/
├── core/helio/
├── microservices/
├── infra/
├── helm/ggtesla/
├── argocd/
├── .github/workflows/
├── docs/
├── api/
├── docker-compose.yml
├── docker-compose.override.local.yml
└── justfile
```

## Локальный запуск
```bash
docker compose up -d
```

Минимальный локальный стек (только NATS/PostgreSQL/Redis/ChromaDB/Vault/Ollama/Scout):
```bash
docker compose -f docker-compose.yml -f docker-compose.override.local.yml up -d
```

## Команды just
```bash
just build
just dev
just prod
just deploy
```

## Тесты
```bash
bash tests/smoke.sh
```
