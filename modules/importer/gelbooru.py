import random
from . import normalise_tags
from modules import schemas,settings
from modules.database import Post
from mimetypes import guess_type
import os
import bs4
import itertools
import requests
import warnings

async def import_gelbooru(
        limit:int|None=settings.IMPORT_GELBOORU_LIMIT,
        searches:list[str]=settings.IMPORT_GELBOORU_SEARCHES,
        gelbooru_url = settings.IMPORT_GELBOORU_WEBSITE,
        ):
    
    posts = []
    for search in searches:
        new_posts = await run_gelbooru_search(gelbooru_url,search,limit)
        posts.extend(new_posts)
    random.shuffle(posts)

    if limit:
        if len(posts) < limit:
            warnings.warn(f"Gelbooru Import: Did not reach intended limit")
        posts = posts[:limit]
    
    for post in posts:
        try:
            await import_post_from_soup(post)
        except KeyError:
            continue

async def run_gelbooru_search(url:str,search:str,limit:int|None) -> list[bs4.BeautifulSoup]:
    url = f"https://{url}/index.php?page=dapi&s=post&q=index"
    url += f"&tags={search}"
    
    found_posts = []
    for x in itertools.count():
        r = requests.get(
            url=url,
            params={
                "limit":1000,
                "pid":x,
            }
        )
        xml = bs4.BeautifulSoup(r.text,"lxml")
        new_posts = xml.find_all('post')
        found_posts.extend(new_posts)
        
        if len(new_posts) != 1000:
            break
        if limit and len(found_posts) >= limit:
            break
    
    return found_posts


async def import_post_from_soup(soup:bs4.BeautifulSoup):
        attrs:dict = soup.attrs
        if await check_post_exists(attrs['md5']):
            return
        
        full = schemas.Image(
            url=attrs['file_url'],
            mimetype=guess_type(attrs['file_url'])[0], # type: ignore
            width=int(attrs['width']),
            height=int(attrs['height']),
        )
        preview = schemas.Image(
            url=attrs['sample_url'],
            mimetype=guess_type(attrs['sample_url'])[0], # type: ignore
            width=int(attrs['sample_width']),
            height=int(attrs['sample_height']),
        )
        thumbnail = schemas.Image(
            url=attrs['preview_url'],
            mimetype=guess_type(attrs['preview_url'])[0], # type: ignore
            width=int(attrs['preview_width']),
            height=int(attrs['preview_height']),
        )
        
        # Tags
        tags = attrs['tags'].split(' ')
        if attrs['rating'] == 's':
            tags.append('rating:safe')
        tags = normalise_tags(tags)
        
        # Type
        TYPE_LOOKUP = {
            ".mp4":"video",
            ".webm":"video",
            ".png":"image",
            ".jpg":"image",
            ".jpeg":"image",
            ".gif":"animation",
        }
        _,ext = os.path.splitext(attrs['file_url'])
        media_type = TYPE_LOOKUP.get(ext,'unknown')
        if media_type == 'unknown':
            return
        
        post_obj = schemas.Post(
            id=Post.get_unused_id(),
            uploader=0,
            media_type=media_type,
            full=full,
            preview=preview,
            thumbnail=thumbnail,
            md5s=[attrs.get('md5',''*24)],
            tags=tags,
            )
        Post.create(post_obj)


async def check_post_exists(md5):
    query = schemas.Post_Query(md5=md5)
    return bool(Post.search(query))
