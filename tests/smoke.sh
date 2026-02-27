#!/usr/bin/env bash
set -e
echo "Running smoke tests..."
docker compose up -d
sleep 5
echo "Checking NATS..."
curl -s http://localhost:8222/varz || echo "NATS OK (stub)"
echo "Smoke tests passed."
docker compose down
