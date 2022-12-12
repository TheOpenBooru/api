from . import parsing
from modules import settings, schemas, posts
from modules.importers import DownloadFailure, Downloader, utils
from urllib.parse import parse_qs, urlparse
import bs4
import requests


class GelbooruDownloader(Downloader):
    _hostname: str
    _api_hostname: str
    def __init__(self):
        requests.get("https://" + self._hostname, timeout=2)


    def is_valid_url(self, url: str) -> bool:
        return url.startswith(f"https://{self._hostname}/index.php?page=post&s=view&id=")


    async def download_url(self, url:str) -> list[schemas.Post]:
        id = await self.extract_id(url)
        post_data = await self.download_post(id)
        
        file_url = post_data["file_url"]
        data, filename = await utils.download_url(file_url)
        post = await posts.generate(data,filename)
        post = posts.apply_edit(
            post=post,
            tags=parsing.get_tags(post_data),
            sources=parsing.get_sources(post_data),
            rating=parsing.get_rating(post_data),
        )
        return [post]


    @staticmethod
    async def extract_id(url:str) -> int:
        try:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            id = query["id"][0]
            id = int(id)  # type: ignore
            return id
        except Exception:
            raise DownloadFailure("Could not extract ID from the URL")


    async def download_post(self, id: int) -> dict:
        url = f"https://{self._api_hostname}/index.php?page=dapi&s=post&q=index"
        try:
            r = requests.get(url,params={'id': id})
        except Exception:
            raise DownloadFailure("Gelbooru API Error")
        
        soup = bs4.BeautifulSoup(r.text, 'xml')
        tag = soup.find('post')
        if not isinstance(tag, bs4.Tag):
            raise DownloadFailure("Gelbooru API Error")
    
        data = tag.attrs
        
        if data["file_url"] == "":
            raise DownloadFailure("Gelbooru API Error")
        
        return data

class SafebooruDownloader(GelbooruDownloader):
    _hostname = "safebooru.org"
    _api_hostname = "safebooru.org"


class Rule34Downloader(GelbooruDownloader):
    _hostname = "rule34.xxx"
    _api_hostname = "api.rule34.xxx"
