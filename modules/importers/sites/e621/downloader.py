from . import parsing
from modules import settings, schemas, posts
from modules.importers import Downloader, utils, DownloadFailure
import re
import requests


class E621Downloader(Downloader):
    _hostname: str = "e621.net"

    def is_valid_url(self,url:str) -> bool:
        return f"https://{self._hostname}/posts/".startswith(url)


    async def download_url(self,url:str) -> list[schemas.Post]:
        id = self.id_from_url(url)
        try:
            r = requests.get(f"https://{self._hostname}/posts/{id}.json")
            raw_data = r.json()
        except Exception:
            raise DownloadFailure("Could not find post")

        data, filename = await utils.download_url(raw_data["file"]["url"]) # type: ignore
        post = await posts.generate(
            data=data,
            filename=filename,
            additional_tags=parsing.get_tags(raw_data),
        )
        post.sources=parsing.get_sources(raw_data)
        post.rating=parsing.get_rating(raw_data)
        return [post]


    def id_from_url(self, url:str) -> int:
        regex_hostname = self._hostname.replace(".","\\.")
        regex = f"^https:\\/\\/{regex_hostname}\\/posts\\/[0-9]+"
        id_match = re.match(regex, url)
        if id_match == None:
            raise DownloadFailure("Could not find post id in url")
        
        id = id_match.group().split("/")[-1]
        id = int(id)
        return id


class E926Downloader(Downloader):
    _hostname: str = "e926.net"