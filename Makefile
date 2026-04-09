PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: install format lint typecheck test integration-test check migrate migrate-down run-api run-sim compose-up compose-down docker-build

install:
	$(PIP) install -e .[dev]

format:
	ruff format .

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy app

test:
	pytest -m "not integration"

integration-test:
	pytest -m integration

check: lint typecheck test

migrate:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

run-api:
	python -m app.services.api.main

run-sim:
	python -m app.services.strategy_runner.main

compose-up:
	docker compose -f docker-compose.yml up --build -d

compose-down:
	docker compose -f docker-compose.yml down

docker-build:
	docker build -f docker/api.Dockerfile -t btp-api:local .
	docker build -f docker/runner.Dockerfile -t btp-runner:local .
	docker build -f docker/reconciler.Dockerfile -t btp-reconciler:local .
