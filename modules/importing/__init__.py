import asyncio
from .base import LocalImporter, URLImporter, ImportFailure, BaseImporter as _BaseImporter
from .utils import _normalise_tag,_normalise_tags, _predict_media_type
from .files import Files
from .safebooru import Safebooru
from .hydrus import Hydrus
from .tubmlr import Tumblr

async def import_all():
    importers = [
        Files(),
        Hydrus(),
        Safebooru(),
        Tumblr(),
    ]
    for importer in importers:
        if importer.enabled:
            await importer.import_default()