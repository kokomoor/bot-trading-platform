#!/usr/bin/env bash
set -euo pipefail

: "${BTP_TEST_DATABASE_URL:?Set BTP_TEST_DATABASE_URL}"
pytest -m integration
