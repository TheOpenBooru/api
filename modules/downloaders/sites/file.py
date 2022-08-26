from . import utils, Downloader, DownloadFailure
from modules import settings, schemas, posts
import os
from urllib.parse import urlparse

VALID_FILE_EXTENTIONS = {'.png', '.jpg', '.jpef', '.webp', '.gif', '.webm' ,'.mp4'}
class File(Downloader):
    enabled = settings.DOWNLOADER_FILE_ENABLED
    functional = True
    def __init__(self):
        pass
    
    def is_valid_url(self,url:str) -> bool:
        url_struct = urlparse(url)
        _, ext = os.path.splitext(url_struct.path)
        is_file_valid = ext in VALID_FILE_EXTENTIONS
        return is_file_valid


    async def download_url(self,url:str) -> list[schemas.Post]:
        try:
            data, filename = utils.download_url(url,timeout=10)
            post = await posts.generate(data, filename)
        except Exception:
            raise DownloadFailure("Could Not Generate Post")
        
        return [post]
