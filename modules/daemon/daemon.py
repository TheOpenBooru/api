from . import schedule_task
from modules import importers, tags, settings
from modules.importers import Hydrus, Files, Rule34, Safebooru, E621
from datetime import timedelta, datetime
import logging


def run_daemon():
    logging.info("Starting Daemon Threads")
    
    schedule_task(tags.regenerate_count, timedelta(seconds=settings.TAGS_TIME_BETWEEN_REGENERATION))
    schedule_task(tags.regenerate_namespaces, timedelta(seconds=settings.TAGS_TIME_BETWEEN_REGENERATION))
    
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
            
            schedule_task(importer.load, importer.time_between_runs)
    except Exception as e:
        logging.exception(e)
