#!/bin/bash

# Start script for the application

set -e

echo "Starting FastAPI application..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

