from functools import cache
from . import Files, Hydrus, Safebooru, Tumblr, Twitter, BaseImporter, URLImporter, ImportFailure
from modules.schemas import Post
import logging


async def import_all():
    for importer in _get_importers():
        await importer.load_default()


async def import_url(url:str) -> list[Post]:
    """Raises:
    - ImportFailure: **Description**
    """
    for importer in _get_importers():
        if not isinstance(importer, URLImporter):
            continue
        elif not importer.is_valid_url(url):
            continue
        else:
            posts = await importer.import_url(url)
            return posts

    raise ImportFailure("No Importer")


@cache
def _get_importers() -> list[BaseImporter]:
    importers_classes = [Files, Hydrus, Safebooru, Tumblr, Twitter]
    working_importers = []

    for importer_class in importers_classes:
        if not importer_class.enabled:
            continue
        
        importer = importer_class()
        if not importer.functional:
            logging.warning(f"Importer {importer.name} was not functional")
            continue
        
        working_importers.append(importer)
    
    return working_importers

