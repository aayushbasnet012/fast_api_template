# Scheduler Documentation

This project includes both **Celery** for distributed task processing and **APScheduler** for in-process scheduled jobs.

## APScheduler

APScheduler is used for scheduled jobs that run within the FastAPI application process.

### Configuration

APScheduler is configured in `app/workers/scheduler.py` and automatically started when the application starts.

### Adding Scheduled Jobs

Edit `app/workers/tasks.py` to add your scheduled jobs:

```python
from app.workers.scheduler import scheduler

def my_scheduled_job():
    """Your scheduled job."""
    print("Job executed")

# Add job to scheduler
scheduler.add_job(
    my_scheduled_job,
    "interval",  # or "cron", "date"
    minutes=5,
    id="my_job",
    replace_existing=True,
)
```

### Job Triggers

#### Interval Trigger
Run a job at regular intervals:

```python
scheduler.add_job(
    my_job,
    "interval",
    minutes=5,  # or hours=1, seconds=30
    id="interval_job",
)
```

#### Cron Trigger
Run a job at specific times:

```python
scheduler.add_job(
    my_job,
    "cron",
    hour=0,      # Run at midnight
    minute=0,
    day_of_week="mon",  # Every Monday
    id="cron_job",
)
```

#### Date Trigger
Run a job once at a specific time:

```python
from datetime import datetime

scheduler.add_job(
    my_job,
    "date",
    run_date=datetime(2024, 12, 25, 12, 0, 0),
    id="date_job",
)
```

### Async Jobs

APScheduler supports async jobs:

```python
async def my_async_job():
    """Async scheduled job."""
    await some_async_operation()

scheduler.add_job(
    my_async_job,
    "interval",
    hours=1,
    id="async_job",
)
```

## Celery

Celery is used for distributed task processing and background jobs.

### Configuration

Celery requires Redis or RabbitMQ as a message broker. Configure in `.env`:

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Defining Tasks

Tasks are defined in `app/workers/tasks.py`:

```python
from app.workers.tasks import celery_app

@celery_app.task(name="my_celery_task")
def my_celery_task(param1, param2):
    """Celery task."""
    # Your task logic
    return result
```

### Running Celery Worker

Start a Celery worker:

```bash
celery -A app.workers.tasks.celery_app worker --loglevel=info
```

### Calling Tasks

From your application code:

```python
from app.workers.tasks import my_celery_task

# Call task asynchronously
result = my_celery_task.delay(param1, param2)

# Call task synchronously (blocking)
result = my_celery_task(param1, param2)
```

### Scheduled Tasks (Celery Beat)

To schedule Celery tasks, use Celery Beat:

1. Create a beat schedule in `app/workers/tasks.py`:

```python
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "daily-task": {
        "task": "my_celery_task",
        "schedule": crontab(hour=0, minute=0),  # Daily at midnight
    },
}
```

2. Start Celery Beat:

```bash
celery -A app.workers.tasks.celery_app beat --loglevel=info
```

## When to Use Which?

- **Use APScheduler** for:
  - Simple scheduled jobs within the application
  - Jobs that need to run in the same process
  - Lightweight periodic tasks

- **Use Celery** for:
  - Heavy computational tasks
  - Tasks that need to run on separate workers
  - Distributed task processing
  - Long-running background jobs

## Docker Setup

The docker-compose.yml includes Redis for Celery. Both schedulers will work out of the box when the application starts.

