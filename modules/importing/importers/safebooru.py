from . import utils, URLImporter, ImportFailure
from modules import settings, schemas, database
from urllib.parse import parse_qs, urlparse
from typing import Any, Union
from tqdm import tqdm
from datetime import datetime
import bs4
import itertools
import requests


class Safebooru(URLImporter):
    name = "Safebooru"
    enabled = settings.IMPORT_SAFEBOORU_ENABLED
    def __init__(self):
        try:
            requests.get("https://safebooru.org/",timeout=2)
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self,url:str) -> bool:
        return url.startswith("https://safebooru.org/index.php?page=post&s=view&id=")


    async def import_url(self,url:str) -> list[schemas.Post]:
        try:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            id = query['id']
        except Exception:
            raise ImportFailure("Could not extract ID from the URL")
        
        url = "https://safebooru.org/index.php?page=dapi&s=post&q=index"
        r = requests.get(url,params={'id':id})
        soup = bs4.BeautifulSoup(r.text,'html.parser')
        tag = soup.find('post')
        post = await post_from_tag(tag)
        return [post]


    async def load_default(self):
        if settings.IMPORT_SAFEBOORU_IMPORT == False:
            return
        
        limit = settings.IMPORT_SAFEBOORU_LIMIT
        searches = settings.IMPORT_SAFEBOORU_SEARCHES
        
        posts = []
        for search in searches:
            new_posts = await run_safebooru_search(search,limit)
            posts.extend(new_posts)
            if limit and len(posts) > limit:
                break

        if limit:
            posts = posts[:limit]
        
        for post in tqdm(posts, desc="Importing From Safebooru"):
            try:
                post = await post_from_tag(post)
                database.Post.insert(post)
            except Exception as e:
                continue


async def run_safebooru_search(search:str,limit:Union[int,None]) -> list[bs4.BeautifulSoup]:
    url = f"https://safebooru.org/index.php?page=dapi&s=post&q=index&tags={search}"
    found_posts = []
    for x in itertools.count():
        r = requests.get(
            url=url,
            params={
                "limit":1000,
                "pid":x,
            }
        )
        xml = bs4.BeautifulSoup(r.text,"xml")
        new_posts = xml.find_all('post')
        found_posts.extend(new_posts)
        
        if len(new_posts) != 1000:
            break
        if limit and len(found_posts) >= limit:
            break
    
    return found_posts


async def post_from_tag(soup:bs4.Tag) -> schemas.Post:
    attrs:dict[str,Any] = soup.attrs
    if database.Post.md5_exists(attrs['md5']):
        raise ImportFailure("Post Already Exists")
    
    tags = utils.normalise_tags(attrs['tags'].split(' '))
    if attrs['source']:
        source = attrs['source']
    else:
        source = f"https://safebooru.org/index.php?page=post&s=view&id={attrs['id']}"
    
    full,preview,thumbnail = construct_images(attrs)
    hashes = schemas.Hashes(md5s=[attrs['md5']])
    post = schemas.Post(
        id=database.Post.get_new_id(),
        created_at=get_date(attrs['created_at']),
        upvotes=int(attrs['score'] or "0"),
        tags=tags,
        source=source,
        media_type=utils.predict_media_type(attrs['file_url']),
        hashes=hashes,
        full=full,
        preview=preview,
        thumbnail=thumbnail,
    )
    return post


def get_date(dateString:str) -> int:
    format = "%a %b %d %H:%M:%S %z %Y"
    date = datetime.strptime(dateString,format)
    timestamp = int(date.timestamp())
    return timestamp


def construct_images(attrs:dict) -> tuple[schemas.Image,schemas.Image,schemas.Image]:
    full = schemas.Image(
        url=attrs['file_url'],
        width=attrs['width'],
        height=attrs['height'],
        mimetype=utils.guess_mimetype(attrs['file_url']),
    )
    preview = schemas.Image(
        url=attrs['sample_url'],
        width=attrs['sample_width'],
        height=attrs['sample_height'],
        mimetype=utils.guess_mimetype(attrs['sample_url']),
    )
    thumbnail = schemas.Image(
        url=attrs['preview_url'],
        width=attrs['preview_width'],
        height=attrs['preview_height'],
        mimetype=utils.guess_mimetype(attrs['preview_url']),
    )
    return full, preview, thumbnail

