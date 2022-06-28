from . import URLImporter, ImportFailure, _normalise_tags
from modules import settings, posts
from urllib.parse import urlparse
from typing import Any
from tqdm import tqdm
import pytumblr
import re
import requests

class Tumblr(URLImporter):
    name = "Tumblr"
    enabled = settings.IMPORT_TUMBLR_ENABLED
    def __init__(self):
        try:
            self.client = pytumblr.TumblrRestClient(
                consumer_key=settings.IMPORT_TUMBLR_KEY,
                consumer_secret = settings.IMPORT_TUMBLR_SECRET,
            )
        except Exception:
            self.functional = False
        else:
            self.functional = True
    
    
    async def import_default(self):
        all_posts = []
        for blogname in settings.IMPORT_TUMBLR_BLOGS:
            blog_posts =[]
            blog_posts.extend(self.client.posts(blogname, type="photo", limit=100)['posts'])
            blog_posts.extend(self.client.posts(blogname, type="video", limit=100)['posts'])
            for post in blog_posts:
                if post["type"] not in ("photo","video"):
                    continue
                else:
                    all_posts.append(post)
        
        
        for post in tqdm(all_posts, desc="Importing From Tumblr"):
            try:
                await self._import_post(post)
            except posts.PostExistsException:
                pass


    def is_valid_url(self,url:str):
        hostname = urlparse(url).hostname or ""
        return hostname in ["tmblr.co"] or hostname.endswith("tumblr.com")

    
    async def import_url(self,url:str):
        url_data = await self._extract_url_info(url)
        blogname, id = url_data['blogname'], url_data['id']
        if id == None:
            posts = self.client.posts(blogname,id=id)
        else:
            posts = self.client.posts(blogname,id=id)
        
        if len(posts) == 0:
            raise ImportFailure("No posts found")
        else:
            await self._import_post(posts)


    async def _extract_url_info(self,url:str) -> dict[str,str]:
        ID_REGEX = r"(?<=http?s:\/\/[a-z]*.tumblr.com/post/)[0-9]*"
        id_match = re.match(ID_REGEX,url)
        if id_match == None:
            raise ImportFailure("Couldn't parse Tumblr URL, no blogname")
        
        id = id_match.group()
        
        blogname = urlparse(url).hostname
        return {
            'id': id,
            'blogname': blogname,
        } # type: ignore


    async def _import_post(self,post:dict[str,Any]):
        source = post['post_url']
        tags = post['tags']
        tags = _normalise_tags(tags)
        if post["type"] == "photo":
            return
            for photo in post['photos']:
                file_url = photo['original_size']['url']
                await self._import_post_data(
                    file_url=file_url,
                    source=source,
                    tags=tags
                )
        elif post["type"] == "video":
            if "video_url" in post:
                await self._import_post_data(
                    file_url=post['video_url'],
                    source=source,
                    tags=tags
                )


    async def _import_post_data(self,file_url:str,source:str,tags:list[str]):
        r = requests.get(file_url)
        data = r.content
        await posts.create(
            data,
            file_url,
            additional_tags=tags,
            source=source
        )
