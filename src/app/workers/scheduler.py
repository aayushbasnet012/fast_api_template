"""APScheduler configuration and setup."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Default job stores
jobstores = {
    "default": MemoryJobStore(),
}

# Default executors
executors = {
    "default": ThreadPoolExecutor(20),
}

# Job defaults
job_defaults = {
    "coalesce": False,
    "max_instances": 3,
}

# Create scheduler instance
scheduler = AsyncIOScheduler(
    jobstores=settings.SCHEDULER_JOBSTORES or jobstores,
    executors=settings.SCHEDULER_EXECUTORS or executors,
    job_defaults=job_defaults,
    timezone=settings.SCHEDULER_TIMEZONE,
)


def job_listener(event):
    """Listener for scheduler events."""
    if event.exception:
        logger.error(f"Job {event.job_id} raised an exception: {event.exception}")
    else:
        logger.info(f"Job {event.job_id} executed successfully")


# Add event listeners
scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


def start_scheduler():
    """Start the scheduler."""
    if not scheduler.running:
        scheduler.start()
        logger.info("APScheduler started")


def shutdown_scheduler():
    """Shutdown the scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("APScheduler shut down")

