#!/usr/bin/env bash
set -euo pipefail

echo "[smoke] checking required files"
test -f docker-compose.yml
test -f justfile
test -f helm/ggtesla/Chart.yaml
test -f infra/nats/nats.conf
echo "[smoke] scaffold checks passed"
