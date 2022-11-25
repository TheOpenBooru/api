from modules import schemas
from modules.attempt import attempt
from modules.importers import Downloader, DownloadFailure, DOWNLOADERS
import logging

intialised_downloaders: list[Downloader] = []


async def download_url(url: str) -> list[schemas.Post]:
    """Raises:
    - ImportFailure: **Description**
    """
    downloader = await get_downloader(url)
    posts = await attempt(3, downloader.download_url, args=(url,))
    return posts


async def get_downloader(url: str):
    if intialised_downloaders == []:
        await intialise_downloaders()
    
    for downloader in intialised_downloaders:
        if not downloader.is_valid_url(url):
            continue
        return downloader

    raise DownloadFailure("No Importer for that URL")


async def intialise_downloaders():
    for _class in DOWNLOADERS:
        try:
            importer = _class()
        except Exception as e:
            downloader_name = _class.__name__.title()
            logging.exception(
                f"Downloader {downloader_name} Failed To Start",
                exc_info=e,
            )
            continue
        else:
            intialised_downloaders.append(importer)
