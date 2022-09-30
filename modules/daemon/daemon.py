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
    if settings.TAGS_IMPORT_TAG_DATA_EVERY:
        create_background_task(
            id="Regen Tag Count",
            function=tags.import_e621_tag_data,
            retry_after=settings.TAGS_IMPORT_TAG_DATA_EVERY,
        )

    
    importers = [Hydrus, Files, Rule34, Safebooru, E621]
    for importer_class in importers:
        if importer_class.enabled == False:
            continue

        name = importer_class.__name__.title()
        try:
            importer = importer_class()
        except Exception:
            logging.warning(f"Importer {name} was not functional")
        else:
            create_background_task(
                id=f"Importing {name}",
                function=importer.load,
                retry_after=importer.time_between_runs
            )