.PHONY: help install install-dev test lint format clean run migrate docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev - Install development dependencies"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean cache files"
	@echo "  make run         - Run the application"
	@echo "  make migrate     - Run database migrations"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"

install:
	pip install -r requirements/base.txt

install-dev:
	pip install -r requirements/dev.txt

test:
	pytest src/tests/ -v --cov=src/app --cov-report=html --cov-report=term

lint:
	ruff check src/
	black --check src/
	mypy src/

format:
	black src/
	ruff check --fix src/

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	alembic upgrade head

docker-up:
	cd docker && docker-compose up -d

docker-down:
	cd docker && docker-compose down

