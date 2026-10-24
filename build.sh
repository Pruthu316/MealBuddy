#!/usr/bin/env bash
# Exit on error
set -o errexit

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Install dependencies
pip install -r requirements.txt

# Collect static files
$PYTHON_CMD manage.py collectstatic --no-input

# Apply database migrations
$PYTHON_CMD manage.py migrate

# Seed catalog if database is empty
$PYTHON_CMD manage.py seed_catalog
