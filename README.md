# FastAPI Template

A production-ready FastAPI project template with authentication, database models, API versioning, and comprehensive testing setup.

## Features

- ✅ FastAPI with async support
- ✅ SQLAlchemy ORM with PostgreSQL
- ✅ Alembic database migrations
- ✅ JWT authentication
- ✅ API versioning (v1)
- ✅ Pydantic settings management
- ✅ APScheduler for scheduled jobs
- ✅ Comprehensive test suite
- ✅ Docker support
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Pre-commit hooks
- ✅ Code formatting (Black, Ruff)
- ✅ Type checking (mypy)

## Project Structure

```
project-name/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline configuration
├── src/
│   ├── app/
│   │   ├── main.py           # FastAPI application factory
│   │   ├── config/           # Configuration files
│   │   ├── api/              # API routes
│   │   ├── core/             # Core utilities (security, exceptions)
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── database/         # Database setup
│   │   ├── middleware/       # Custom middleware
│   │   ├── utils/            # Utility functions
│   │   └── workers/          # APScheduler jobs
│   ├── tests/                # Test suite
│   └── alembic/              # Database migrations
├── docker/                   # Docker configuration
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
└── requirements/             # Python dependencies
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- (Optional) Docker and Docker Compose

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume_backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
make install-dev
# or
pip install -r requirements/dev.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
make migrate
# or
alembic upgrade head
```

6. Start the application:
```bash
make run
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker Setup

1. Start services:
```bash
make docker-up
# or
cd docker && docker-compose up -d
```

2. Stop services:
```bash
make docker-down
# or
cd docker && docker-compose down
```

## Development

### Running Tests

```bash
make test
# or
pytest src/tests/ -v --cov=src/app
```

### Code Formatting

```bash
make format
# or
black src/
ruff check --fix src/
```

### Linting

```bash
make lint
# or
ruff check src/
black --check src/
mypy src/
```

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pre-commit install
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/` - Get all users (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID (admin only)
- `POST /api/v1/users/` - Create user (admin only)
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user (admin only)

### Items
- `GET /api/v1/items/` - Get all items for current user
- `GET /api/v1/items/{item_id}` - Get item by ID
- `POST /api/v1/items/` - Create item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## Environment Variables

See `.env.example` for all available environment variables.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Secret key for JWT tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `CORS_ORIGINS` - Allowed CORS origins
- `SCHEDULER_TIMEZONE` - Timezone for APScheduler (default: UTC)

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Scheduler

This project uses **APScheduler** for scheduled jobs. Jobs run within the FastAPI application process and are started automatically when the application starts. See `docs/scheduler.md` for detailed documentation.

## License

MIT

