from . import utils, Importer, ImportFailure
from modules import settings, schemas, database
from urllib.parse import parse_qs, urlparse
from typing import Any, Union
from tqdm import tqdm
from datetime import datetime
import bs4
import itertools
import requests


class Safebooru(Importer):
    enabled = settings.IMPORTER_SAFEBOORU_ENABLED
    def __init__(self):
        try:
            requests.get("https://safebooru.org/",timeout=2)
        except Exception:
            self.functional = False
        else:
            self.functional = True


    async def load(self, limit:Union[int, None] = settings.IMPORTER_SAFEBOORU_LIMIT):
        searches = settings.IMPORTER_SAFEBOORU_SEARCHES
        
        posts = []
        for search in searches:
            new_posts = await run_safebooru_search(search,limit)
            posts.extend(new_posts)
            if limit and len(posts) > limit:
                break

        post_count = 0
        for post in tqdm(posts, desc="Importing From Safebooru"):
            if limit and post_count >= limit:
                return
            
            try:
                post = await post_from_tag(post)
                database.Post.insert(post)
                post_count += 1
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
    post:dict[str,Any] = soup.attrs
    if database.Post.md5_exists(post['md5']):
        raise ImportFailure("Post Already Exists")
    
    full,preview,thumbnail = construct_images(post)
    return schemas.Post(
        id=database.Post.generate_id(),
        created_at=get_date(post['created_at']),
        upvotes=int(post['score'] or "0"),
        tags=get_tags(post),
        source=get_source(post),
        media_type=utils.predict_media_type(post['file_url']), # type: ignore
        hashes=get_hashes(post),
        full=full,
        preview=preview,
        thumbnail=thumbnail,
    )


def get_tags(post:dict) -> list[str]:
    tag_string = post['tags']
    tags = tag_string.split(' ')
    return utils.normalise_tags(tags)


def get_source(post:dict) -> str:
    if post['source']:
        return post['source']
    else:
        return f"https://safebooru.org/index.php?page=post&s=view&id={post['id']}"


def get_hashes(post:dict) -> schemas.Hashes:
    md5 = post['md5']
    return schemas.Hashes(md5s=[md5])


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

