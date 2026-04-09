#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. Install docker and docker compose plugin first."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Edit secrets before production use."
fi

alembic upgrade head

docker compose -f docker-compose.prod.yml pull || true
docker compose -f docker-compose.prod.yml up --build -d

echo "Deployment complete. Verify health via /health and /ready endpoints."
