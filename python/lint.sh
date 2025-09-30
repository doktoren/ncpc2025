#!/bin/bash

set -e

uv sync --no-install-project

echo "Running ruff linting..."
uv run ruff check --fix

echo "Running mypy type checking..."
uv run mypy --config-file mypy.ini .

echo "Running unit tests..."
uv run pytest
