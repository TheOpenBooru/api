from . import create_background_task
from modules import importers, tags, settings, subscription
from modules.importers import IMPORTERS
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
            id="Regen Tag Data",
            function=tags.import_e621_tag_data,
            retry_after=settings.TAGS_IMPORT_TAG_DATA_EVERY,
        )
    create_background_task(
        id="Check URL Subscriptions",
        function=subscription.check_subscriptions,
        retry_after=settings.SUBSCRIPTIONS_TRY_AFTER,
    )

    
    for _class in IMPORTERS:
        if _class.enabled == False:
            continue

        name = _class.__name__.title()
        try:
            importer = _class()
        except Exception as e:
            logging.warning(f"Importer {name} was not functional")
        else:
            create_background_task(
                id=f"Importing {name}",
                function=importer.load,
                retry_after=importer.time_between_runs
            )