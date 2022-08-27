from . import Downloader, DownloadFailure, utils
from modules import schemas, settings, posts
from urllib.parse import urlparse
from typing import Any
import pytumblr
import re


class Tumblr(Downloader):
    enabled = settings.DOWNLOADER_TUMBLR_ENABLED
    def __init__(self):
        try:
            self.client = pytumblr.TumblrRestClient(
                consumer_key=settings.DOWNLOADER_TUMBLR_KEY,
                consumer_secret = settings.DOWNLOADER_TUMBLR_SECRET,
            )
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self,url:str):
        hostname = urlparse(url).hostname or ""
        return any((
            hostname == ("tumblr.co"),
            hostname == "tumblr.com",
            hostname.endswith(".tumblr.com"),
        ))


    async def download_url(self,url:str) -> list[schemas.Post]:
        blogname, id = await extract_url_info(url)
        if id == None:
            raise DownloadFailure("Cannot Import From Blog, need Post ID")
        
        posts = self.client.posts(blogname,id=id)
        
        if len(posts) == 0:
            raise DownloadFailure("No posts found")
        else:
            posts = await post_from_data(posts)
            return posts


async def extract_url_info(url:str) -> tuple[str,str]:
    """Extracts ID and Blogname from a tumblr URL
    
    Returns:
        - id
        - blogname
    """
    ID_REGEX = r"(?<=http?s:\/\/[a-z]*.tumblr.com/post/)[0-9]*"
    id_match = re.match(ID_REGEX,url)
    if id_match == None:
        raise DownloadFailure("Couldn't parse Tumblr URL, no post ID")
    
    id = id_match.group()
    
    blogname = urlparse(url).hostname
    return id, blogname # type: ignore


async def post_from_data(data:dict[str,Any]) -> list[schemas.Post]:
    source = data['post_url']
    tags = utils.normalise_tags(data['tags'])
    if data["type"] == "photo":
        posts = []
        for photo in data['photos']:
            file_url = photo['original_size']['url']
            post = await import_post_from_data(
                file_url=file_url,
                source=source,
                tags=tags
            )
            posts.append(post)
        return posts

    elif data["type"] == "video":
        post = await import_post_from_data(
            file_url=data['video_url'],
            source=source,
            tags=tags
        )
        return [post]
    else:
        raise DownloadFailure("Could Not Import Post")


async def import_post_from_data(file_url:str,source:str,tags:list[str]) -> schemas.Post:
    data, filepath = utils.download_url(file_url)
    post = await posts.generate(
        data,
        filepath,
        additional_tags=tags,
        source=source
    )
    return post
