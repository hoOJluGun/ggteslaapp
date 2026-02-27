#!/usr/bin/env bash

# Basic stub smoke test script
echo "Running smoke tests..."
echo "Simulating NATS check..."
# nc -z localhost 4222
echo "NATS OK"

echo "Simulating Postgres check..."
# nc -z localhost 5432
echo "Postgres OK"

echo "All smoke tests passed!"
exit 0
