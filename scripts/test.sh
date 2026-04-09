#!/usr/bin/env bash
set -euo pipefail

ruff check .
ruff format --check .
mypy app
pytest -m "not integration"
