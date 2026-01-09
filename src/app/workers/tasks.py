"""Celery tasks and APScheduler jobs."""

from celery import Celery
from app.config.settings import settings
from app.workers.scheduler import scheduler
import logging

logger = logging.getLogger(__name__)

# Celery app configuration
if settings.CELERY_BROKER_URL and settings.CELERY_RESULT_BACKEND:
    celery_app = Celery(
        "worker",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )

    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )

    @celery_app.task(name="example_celery_task")
    def example_celery_task():
        """Example Celery task."""
        logger.info("Celery task executed")
        return "Task completed"
else:
    celery_app = None
    logger.warning("Celery not configured. Set CELERY_BROKER_URL and CELERY_RESULT_BACKEND in settings.")


# APScheduler jobs
def example_scheduled_job():
    """Example APScheduler job."""
    logger.info("Scheduled job executed")
    return "Scheduled job completed"


async def example_async_scheduled_job():
    """Example async APScheduler job."""
    logger.info("Async scheduled job executed")
    return "Async scheduled job completed"


def setup_scheduled_jobs():
    """Setup scheduled jobs."""
    # Example: Run a job every 5 minutes
    # scheduler.add_job(
    #     example_scheduled_job,
    #     "interval",
    #     minutes=5,
    #     id="example_job",
    #     replace_existing=True,
    # )

    # Example: Run a job at specific times (cron)
    # scheduler.add_job(
    #     example_scheduled_job,
    #     "cron",
    #     hour=0,
    #     minute=0,
    #     id="daily_job",
    #     replace_existing=True,
    # )

    # Example: Run an async job
    # scheduler.add_job(
    #     example_async_scheduled_job,
    #     "interval",
    #     hours=1,
    #     id="hourly_async_job",
    #     replace_existing=True,
    # )

    logger.info("Scheduled jobs setup completed")

