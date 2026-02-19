"""APScheduler jobs."""

from app.workers.scheduler import scheduler
import logging

logger = logging.getLogger(__name__)


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
