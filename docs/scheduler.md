# Scheduler Documentation

This project uses **APScheduler** for in-process scheduled jobs.

## APScheduler

APScheduler runs scheduled jobs within the FastAPI application process.

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

## Docker Setup

When running with Docker, the scheduler starts automatically with the application.
