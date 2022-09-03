from . import schedule_task
from modules import importers, tags, settings
from datetime import timedelta
import logging


def run_daemon():
    logging.info("Starting Daemon Threads")
    schedule_task(tags_thread, timedelta(seconds=settings.TAGS_TIME_BETWEEN_REGENERATION))
    schedule_task(importer_thread, timedelta(days=1))


async def tags_thread():
    try:
        tags.regenerate()
    except KeyboardInterrupt:
        print("Manually Skippped Tag Regenerated")
    except Exception as e:
        logging.exception(e)


async def importer_thread():
    try:
        await importers.import_all()
    except Exception as e:
        logging.exception(e)
