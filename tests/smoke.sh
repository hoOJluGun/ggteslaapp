#!/usr/bin/env bash
set -euo pipefail

echo "[smoke] required files"
test -f docker-compose.yml
test -f docker-compose.override.local.yml
test -f justfile
test -f helm/ggtesla/Chart.yaml
test -f helm/ggtesla/templates/service.yaml
test -f infra/nats/nats.conf
test -f infra/vault/vault.hcl
test -f infra/opa/policies.rego
echo "[smoke] scaffold checks passed"
