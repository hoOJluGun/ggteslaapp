# GG Tesla App Platform - Общая Архитектура

## 1. Концепция и Bounded Contexts
Платформа GG Tesla представляет собой Event-Driven Monorepo с единой шиной данных для быстрой интеграции множества клиентских интерфейсов и специфичных корпоративных задач (real-time обновления, AI-чаты, генерация тяжелых отчетов).

### 1.1 HELIO Core (Node.js/TS + Fastify)
Главный шлюз и API-интерфейс для всех HTTP/WebSocket подключений от web-приложений. 
- Роутинг и аутентификация запросов.
- Оркестрация CRUD-операций через PostgreSQL.
- Публикация транзакционных и аналитических событий в NATS.

### 1.2 Микросервисы реального времени (Rust)
- **SFU Service (`sfu-rs`)**: Прием и маршрутизация WebRTC аудио/видео/данных в реальном времени. Интеграция с NATS для уведомлений о начале сессий.
- **CRDT Sync (`crdt-sync-rs`)**: Conflict-free Replicated Data Types для синхронного редактирования документов и статусов несколькими пользователями из разных клиентов без конфликтов.
- **Reporting (`reporting-rs`)**: Тяжелый воркер для обработки аналитики и генерации отчетов.
- **Интеграция с ИИ (Python/Scout)**: Локальная работа с эмбеддингами (ChromaDB) и приватным LLM (Ollama) для AI-фич.

## 2. Контракт событий (Event Contract Pattern)

Все микросервисы общаются через шину NATS JetStream. 
Мы используем стандартизированный формат топиков: `[domain].[entity].[action].[version]`.

### Примеры топиков:
- `user.auth.login.v1` — Успешный вход пользователя.
- `report.generate.start.v1` — Запрос на старт тяжелого отчета.
- `telemetry.vehicle.status.v1` — Real-time метрика авто.

### Единая структура Payload (JSON)
```json
{
  "eventId": "uuid-v4",
  "eventType": "report.generate.start.v1",
  "timestamp": "2026-02-28T00:26:21Z",
  "actorId": "user_123",
  "data": {
    "reportType": "monthly_summary",
    "params": { ... }
  },
  "metadata": {
    "correlationId": "uuid-v4"
  }
}
```

## 3. Показатели SLO/SLI (Надежность)
- **API (HELIO Core)**: Успешность запросов (HTTP 2xx, 3xx) > 99.9%. Латентность 95p < 200ms.
- **Real-Time Pipeline (SFU, NATS)**: Задержка доставки сообщений p99 < 50ms.
- **Availability Infrastructure**: 99.99% аптайм благодаря Kubernetes deployment, liveness probes и ArgoCD self-healing.

## 4. Стратегия безопасности (Security Posture)
- **Secret Management**: Vault для инъекции секретов в Pod'ы через Vault Agent. Приложения не знают секреты до старта.
- **Role-Based Access Control / ABAC**: Все решения принимаются централизованным движком политик (OPA), написанным на Rego. Микросервис `authz-rs` предоставляет кеширующий интерфейс к OPA для других узлов.
