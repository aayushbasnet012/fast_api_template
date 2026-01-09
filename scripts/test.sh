#!/bin/bash

# Test script

set -e

echo "Running tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
pytest src/tests/ -v --cov=src/app --cov-report=html --cov-report=term

echo "Tests completed!"

