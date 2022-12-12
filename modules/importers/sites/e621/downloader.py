from . import parsing, USER_AGENT
from modules import schemas, posts
from modules.importers import Downloader, utils, DownloadFailure
import re
import requests


class E621Downloader(Downloader):
    _hostname: str = "e621.net"

    def is_valid_url(self,url:str) -> bool:
        return url.startswith(f"https://{self._hostname}/posts/")


    async def download_url(self,url:str) -> list[schemas.Post]:
        id = self.id_from_url(url)
        try:
            r = requests.get(
                f"https://{self._hostname}/posts/{id}.json",
                headers={"User-Agent": USER_AGENT}
            )
            json = r.json()
            post_data = json["post"]
        except Exception:
            raise DownloadFailure("Could not find post")

        file_url = post_data["file"]["url"] # type: ignore
        data, filename = await utils.download_url(file_url)
        post = await posts.generate(data,filename)
        post = posts.apply_edit(
            post=post,
            tags=parsing.get_tags(post_data),
            sources=parsing.get_sources(post_data),
            rating=parsing.get_rating(post_data)
        )
        return [post]


    def id_from_url(self, url:str) -> int:
        regex = f"^https:\\/\\/{self._hostname}\\/posts\\/[0-9]+"
        id_match = re.match(regex, url)
        if id_match == None:
            raise DownloadFailure("Could not find post id in url")
        
        id = id_match.group().split("/")[-1]
        id = int(id)
        return id


class E926Downloader(Downloader):
    _hostname: str = "e926.net"