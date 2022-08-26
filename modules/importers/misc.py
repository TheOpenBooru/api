import logging
from . import Hydrus, Files, Rule34, Safebooru, E621, Importer
from logging import warning

async def import_all():
    importers = [Hydrus, Files, Rule34, Safebooru, E621]
    for importer_class in importers:
        if importer_class.enabled == False:
            continue
        
        importer = importer_class()
        name = type(importer).__name__
        if importer.functional == False:
            warning(f"Importer {name} was not functional")
        else:
            try:
                await importer.load()
            except KeyboardInterrupt:
                logging.info(f"Manually Skipped Importing {name}")
