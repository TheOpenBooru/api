from openbooru.modules import settings, schemas, posts, encoding
from openbooru.modules.importers import utils, Downloader, DownloadFailure
import os
from urllib.parse import urlparse

class FileDownloader(Downloader):
    def is_valid_url(self, url:str) -> bool:
        url_struct = urlparse(url)
        _, ext = os.path.splitext(url_struct.path)
        is_file_valid = ext in encoding.ACCEPTED_FILE_EXTENTIONS
        return is_file_valid


    async def download_url(self,url:str) -> list[schemas.Post]:
        try:
            data, filename = await utils.download_url(url,timeout=10)
            post = await posts.generate(data, filename)
            post.sources = [url]
        except Exception:
            raise DownloadFailure("Could Not Generate Post")
        
        return [post]
