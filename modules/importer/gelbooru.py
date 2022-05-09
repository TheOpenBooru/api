from . import normalise_tag
from modules import schemas,settings
from modules.database import Post
from mimetypes import guess_type
import os
import bs4
import itertools
import requests
import warnings

async def import_gelbooru(limit=settings.IMPORT_GELBOORU_LIMIT,tags=settings.IMPORT_GELBOORU_TAGS):
    gelbooru_url = settings.IMPORT_GELBOORU_WEBSITE
    for index in itertools.count():
        if index == 100:
            warnings.warn('Gelbooru Import: Searched more than 100 pages')

        url = f"https://{gelbooru_url}/index.php?page=dapi&s=post&q=index"
        url += f"&tags={'+'.join(tags)}"
        r = requests.get(
            url,
            params={
                "limit":1000,
                "pid":index,
            }
        )
        xml = bs4.BeautifulSoup(r.text,"lxml")
        loaded_posts = xml.find_all("post")
        
        if len(loaded_posts) == 0:
            warnings.warn(f"Gelbooru Import: Did not reach intended limit")
            return
        
        for post in loaded_posts:
            if len(Post.all()) >= limit:
                return
            attrs:dict = post.attrs
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
                url=post.attrs['preview_url'],
                mimetype=guess_type(attrs['preview_url'])[0], # type: ignore
                width=int(attrs['preview_width']),
                height=int(attrs['preview_height']),
            )
            # Tags
            tags = attrs['tags'].split(' ')
            tags = [normalise_tag(tag) for tag in tags]
            if attrs['rating'] == 's':
                post.append('rating:safe')
            tags = list(set(tags))
            if '' in tags:
                tags.remove('')
            
            # Type
            TYPE_LOOKUP = {
                ".mp4":"video",
                ".webm":"video",
                ".png":"image",
                ".jpg":"image",
                ".jpeg":"image",
                ".gif":"animation",
            }
            _,ext = os.path.splitext(post.attrs['file_url'])
            media_type = TYPE_LOOKUP.get(ext,'unknown')
            if media_type == 'unknown':
                continue
            
            post_obj = schemas.Post(
                id=Post.get_unused_id(),
                uploader=0,
                media_type=media_type,
                full=full,
                preview=preview,
                thumbnail=thumbnail,
                md5s=[post.attrs.get('md5',''*24)],
                tags=tags,
                )
            Post.create(post_obj)
            
