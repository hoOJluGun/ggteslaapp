# GG Tesla App Platform Scaffold

Production-oriented full-stack scaffold for a HELIO core with web, Telegram bot, desktop clients, realtime infrastructure, and cloud-native deployment.

## Included
- React/TypeScript PWA (`apps/web`) with Dockerfile.
- HELIO core (`core/helio`) using Node.js/TypeScript.
- Rust microservices (`microservices/*`) for SFU, CRDT sync, reporting, and authz.
- Telegram bot (`apps/telegram-bot`) on the same NATS + JetStream event bus.
- macOS and Windows client scaffolding.
- Local infrastructure via Docker Compose + override.
- Helm chart + Argo CD app spec.
- GitHub Actions CI/CD pipeline.
- Vault + OPA governance scaffolding.
- Just commands for build/dev/prod/deploy.

## Directory Structure

```text
.
├── .github/workflows/ci-cd.yml
├── api/openapi.yaml
├── apps
│   ├── macos/src/main.rs
│   ├── telegram-bot/src/index.ts
│   ├── web
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/main.tsx
│   └── windows/src/main.ps1
├── argocd/application.yaml
├── core/helio/src/index.ts
├── docker-compose.override.local.yml
├── docker-compose.yml
├── docs
│   ├── API.md
│   ├── CONTRIBUTING.md
│   └── SECURITY.md
├── helm/ggtesla
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/deployment.yaml
├── infra
│   ├── nats/nats.conf
│   ├── opa/policies.rego
│   └── vault/vault.hcl
├── justfile
├── microservices
│   ├── authz-rs/src/main.rs
│   ├── crdt-sync-rs/src/main.rs
│   ├── reporting-rs/src/main.rs
│   └── sfu-rs/src/main.rs
└── tests/smoke.sh
```

## Local Development

```bash
docker compose up -d
```

For minimal local stack only:

```bash
docker compose -f docker-compose.yml -f docker-compose.override.local.yml up -d
```

## Tests

```bash
just build
just dev
bash tests/smoke.sh
```

See also:
- [Contributing](docs/CONTRIBUTING.md)
- [Security](docs/SECURITY.md)
- [API](docs/API.md)
