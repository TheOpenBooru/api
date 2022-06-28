import asyncio
import logging
from .base import LocalImporter, URLImporter, ImportFailure, BaseImporter
from .utils import _normalise_tag,_normalise_tags, _predict_media_type
from .files import Files
from .safebooru import Safebooru
from .hydrus import Hydrus
from .tubmlr import Tumblr

async def import_all():
    importers: list[BaseImporter] = [
        Files(),
        Hydrus(),
        Safebooru(),
        Tumblr(),
    ]
    for importer in importers:
        if importer.enabled:
            if importer.functional:
                await importer.import_default()
            else:
                logging.warning(f"Importer {importer.name} was not functional")