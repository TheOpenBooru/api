import warnings
from . import normalise_tag
from modules import schemas
from modules.database import Post
from mimetypes import guess_type
import os
import requests
import bs4

async def import_safebooru(count:int = 100):
    page = 0 
    while len(Post.all()) < count:
        page += 1
        if page == 100:
            warnings.warn('Safebooru Searched more than 100 pages')
        
        url = "https://safebooru.org/index.php?page=dapi&s=post&q=index" \
              "&tags=d.va_(overwatch)+sort:score+-cleavage+-feet+-pregnant+-*panties"
        r = requests.get(
            url,
            params={
                "limit":count,
                "pid":page,
            }
        )
        xml = bs4.BeautifulSoup(r.text,"lxml")
        loaded_posts = xml.find_all("post")
        
        if len(loaded_posts) == 0:
            warnings.warn(f"SafeBooru: Did not reach {count} posts")
            return
        
        for post in loaded_posts:
            attrs = post.attrs
            full = schemas.Image(
                url=attrs['file_url'],
                mimetype=guess_type(attrs['file_url'])[0],
                width=int(post.attrs['width']),
                height=int(post.attrs['height']),
            )
            preview = schemas.Image(
                url=attrs['sample_url'],
                mimetype=guess_type(post.attrs['sample_url'])[0],
                width=int(post.attrs['sample_width']),
                height=int(post.attrs['sample_height']),
            )
            thumbnail = schemas.Image(
                url=post.attrs['preview_url'],
                mimetype=guess_type(post.attrs['preview_url'])[0],
                width=int(post.attrs['preview_width']),
                height=int(post.attrs['preview_height']),
            )
            # Tags
            tags = post.attrs.get('tags','').split(' ')
            tags = [normalise_tag(tag) for tag in tags]
            tags.append('')
            tags = list(set(tags))
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
