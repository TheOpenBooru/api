from . import create_background_task
from modules import importers, tags, settings
from modules.importers import Hydrus, Files, Rule34, Safebooru, E621
from datetime import timedelta, datetime
import logging


def run_daemon():
    logging.info("Starting Daemon Threads")
    if settings.TAGS_REGEN_COUNT_EVERY:
        create_background_task(
            id="Regen Tag Count",
            function=tags.regenerate_count,
            retry_after=settings.TAGS_REGEN_COUNT_EVERY,
        )
        create_background_task(
            id="Updated Namespaces",
            function=tags.regenerate_namespaces,
            # e621 namespace dumps only regen every day
            retry_after=timedelta(days=1).total_seconds(), 
        )
    schedule_importers()


def schedule_importers():
    importers = [Hydrus, Files, Rule34, Safebooru, E621]
    try:
        for importer_class in importers:
            name = importer_class.__name__
            
            if importer_class.enabled == False:
                continue

            try:
                importer = importer_class()
            except Exception:
                logging.warning(f"Importer {name} was not functional")
                continue
            
            create_background_task(
                id=f"Importing {name}",
                function=importer.load,
                retry_after=importer.time_between_runs
            )
    except Exception as e:
        logging.exception(e)
