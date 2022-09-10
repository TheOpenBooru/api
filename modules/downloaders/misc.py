from . import Downloader, DownloadFailure
from . import Safebooru, Tumblr, Twitter, Youtube, E621, Rule34, File
from functools import cache
from modules.schemas import Post
import logging


async def download_url(url:str) -> list[Post]:
    """Raises:
    - ImportFailure: **Description**
    """
    importers = _get_importers()
    for importer in importers:
        if not isinstance(importer, Downloader):
            continue
        elif not importer.is_valid_url(url):
            continue
        else:
            posts = await importer.download_url(url)
            return posts

    raise DownloadFailure("No Importer for that URL")


@cache
def _get_importers() -> list[Downloader]:
    importers_classes = [Safebooru, Tumblr, Twitter, Youtube, E621, Rule34, File]
    working_importers = []

    for importer_class in importers_classes:
        if not importer_class.enabled:
            continue
        
        importer = importer_class()
        if not importer.functional:
            logging.warning(f"Downloader {type(importer).__name__} was not functional")
            continue
        
        working_importers.append(importer)
    
    return working_importers