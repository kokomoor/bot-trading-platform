PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: install format lint typecheck test check up down

install:
	$(PIP) install -e .[dev]

format:
	ruff format .

lint:
	ruff check .

typecheck:
	mypy app

test:
	pytest

check: lint typecheck test

up:
	docker compose up --build -d

down:
	docker compose down
