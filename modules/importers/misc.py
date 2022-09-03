from . import Hydrus, Files, Rule34, Safebooru, E621, Importer
import logging
from datetime import datetime
from logging import warning

async def import_all():
    importers = [Hydrus, Files, Rule34, Safebooru, E621]
    for importer_class in importers:
        if importer_class.enabled == False:
            continue

        name = importer_class.__name__
        
        try:
            importer = importer_class()
        except Exception:
            warning(f"Importer {name} was not functional")
            continue

        start = datetime.now()
        logging.info(f"Started Importing {name}")
        await importer.load()
        end = datetime.now()
        logging.info(f"Finsihed Importing {name} in {(end - start).total_seconds():.2f} seconds")
