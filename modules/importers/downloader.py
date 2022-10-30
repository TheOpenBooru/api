from modules import schemas
from modules.importers import Downloader, DownloadFailure, DOWNLOADERS
import logging

intiialised_downloaders: list[Downloader] = []


async def download_url(url:str) -> list[schemas.Post]:
    """Raises:
    - ImportFailure: **Description**
    """
    if intiialised_downloaders == []:
        await intialise_importers()
    
    downloader = await get_downloader(url)
    posts = await downloader.download_url(url)
    return posts


async def get_downloader(url: str):
    for downloader in intiialised_downloaders:
        if not downloader.is_valid_url(url):
            continue
        return downloader
    
    raise DownloadFailure("No Importer for that URL")


async def intialise_importers():
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
            intiialised_downloaders.append(importer)