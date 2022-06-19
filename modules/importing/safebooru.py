from . import _normalise_tags, _predict_media_type, URLImporter, ImportFailure
from modules import settings, posts, database
from urllib.parse import parse_qs, urlparse
from mimetypes import guess_type
from typing import Union
from tqdm import tqdm
import bs4
import itertools
import requests


class Safebooru(URLImporter):
    enabled = settings.IMPORT_SAFEBOORU_ENABLED
    def __init__(self):
        try:
            requests.get("https://safebooru.org/",timeout=5)
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self,url:str) -> bool:
        return url.startswith("https://safebooru.org/index.php?page=post&s=view&id=")


    async def import_url(self,url:str):
        try:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            id = query['id']
        except Exception:
            raise ImportFailure
        
        url = "https://safebooru.org/index.php?page=dapi&s=post&q=index"
        r = requests.get(
            url,
            params={'id':id}
        )
        soup = bs4.BeautifulSoup(r.text,'html.parser')
        await _import_post_from_soup(soup)


    async def import_default(self):
        limit = settings.IMPORT_SAFEBOORU_LIMIT
        searches = settings.IMPORT_SAFEBOORU_SEARCHES
        
        posts = []
        for search in searches:
            new_posts = await _run_safebooru_search(search,limit)
            posts.extend(new_posts)
            if limit and len(posts) > limit:
                break

        if limit:
            posts = posts[:limit]
        
        for post in tqdm(posts, desc="Import From Safebooru"):
            try:
                await _import_post_from_soup(post)
            except KeyError:
                continue


async def _run_safebooru_search(search:str,limit:Union[int,None]) -> list[bs4.BeautifulSoup]:
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


async def _import_post_from_soup(soup:bs4.BeautifulSoup):
    attrs:dict = soup.attrs
    try:
        database.Post.getByMD5(attrs['md5'])
    except KeyError:
        pass
    else:
        return
        
    
    tags = _normalise_tags(attrs['tags'].split(' '))
    tags.append('rating:safe')
    source = f"https://safebooru.org/index.php?page=post&s=view&id={attrs['id']}"

    file_url = attrs['file_url']
    r = requests.get(file_url)
    data = r.content
    try:
        await posts.create(
            data=data,
            filename=file_url,
            additional_tags=tags,
            source=source,
        )
    except posts.PostExistsException:
        pass
