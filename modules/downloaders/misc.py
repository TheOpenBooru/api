from . import Downloader, DownloadFailure
from . import Safebooru, Tumblr, Twitter, Youtube, E621, Rule34, File
from modules.schemas import Post
import logging

importers = []

async def download_url(url:str) -> list[Post]:
    """Raises:
    - ImportFailure: **Description**
    """
    for importer in importers:
        if not isinstance(importer, Downloader):
            continue
        elif not importer.is_valid_url(url):
            continue
        else:
            posts = await importer.download_url(url)
            return posts

    raise DownloadFailure("No Importer for that URL")


def load_importers() -> list[Downloader]:
    importers_classes = [Safebooru, Tumblr, Twitter, Youtube, E621, Rule34, File]

    for importer_class in importers_classes:
        if not importer_class.enabled:
            continue
        
        try:
            importer = importer_class()
        except Exception as e:
            downloader_name = importer_class.__name__.title()
            logging.exception(
                f"Downloader {downloader_name} Failed To Start",
                exc_info=e,
            )
        else:
            importers.append(importer)
    
    return importers