from . import utils, Downloader, DownloadFailure
from modules import settings, schemas, database, posts
from urllib.parse import parse_qs, urlparse
import logging
from tqdm import tqdm
from datetime import datetime
import bs4
import requests
import ujson


class Rule34(Downloader):
    enabled = settings.DOWNLOADER_RULE34_ENABLED
    def __init__(self):
        # Test Rule34 Connection
        requests.get("https://rule34.xxx/",timeout=2)


    def is_valid_url(self,url:str) -> bool:
        return url.startswith("https://rule34.xxx/index.php?page=post&s=view&id=")


    async def download_url(self,url:str) -> list[schemas.Post]:
        try:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            id = query["id"][0]
        except Exception:
            raise DownloadFailure("Could not extract ID from the URL")
        
        post_data = post_from_id(id)
        tags = extract_tags(post_data)
        source = extract_source(post_data)
        url = post_data["file_url"]
        
        data,filename = utils.download_url(url)
        post = await posts.generate(data,filename,
            additional_tags=tags,
            source=source,
        )
        return [post]


def post_from_id(id:str) -> dict:
    url = "https://rule34.xxx/index.php?page=dapi&s=post&q=index&id=6577501"
    r = requests.get(
        url=url,
        params={"id": id}
    )
    soup = bs4.BeautifulSoup(r.text,features="lxml-xml")
    tag: bs4.Tag = soup.find("post") # type: ignore
    
    if tag == None:
        raise DownloadFailure("Rule34 Post Does Not Exist")
    else:
        return tag.attrs


def extract_tags(post_data:dict) -> list[str]:
    tag_string = post_data["tags"]
    tags = tag_string.split(" ")
    tags = utils.normalise_tags(tags)
    return tags


def extract_source(post_data:dict) -> str:
    id = post_data["id"]
    source = post_data["source"]
    if source:
        return source
    else:
        return f"https://rule34.xxx/index.php?page=post&s=view&id={id}"
