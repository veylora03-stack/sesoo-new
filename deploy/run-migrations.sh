#!/bin/bash
# Run database migrations manually in production.
# The "migrate" service runs once (restart: "no") and waits for a healthy db.
set -e
cd "$(dirname "$0")/.."
docker compose run --rm migrate