from . import schedule_task
from modules import importers, tags
from datetime import timedelta
import logging


def run_daemon():
    logging.info("Starting Daemon Threads")
    schedule_task(tags_thread, timedelta(seconds=5))
    schedule_task(importer_thread, timedelta(hours=1))


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
