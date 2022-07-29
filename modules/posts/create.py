from . import generate
from modules import database, settings
from modules.tags import generate_ai_tags
import hashlib
import mimetypes
from typing import Union

class PostExistsException(Exception):
    pass

async def create(data:bytes,filename:str,
        use_ai_tags:bool=settings.TAGS_TAGGING_SERVICE_ENABLED,
        uploader_id:Union[int,None] = None,
        additional_tags:Union[list[str],None] = None,
        source:Union[str,None] = None,
        rating:Union[str,None] = None,
        ):
    if PostExists(data):
        raise PostExistsException
    
    post = await generate(data,filename,use_ai_tags,uploader_id,additional_tags,source,rating)

    database.Post.insert(post)
    if uploader_id:
        database.User.create_post(uploader_id,post.id)
    
    return post


def PostExists(data:bytes) -> bool:
    md5 = hashlib.md5(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    
    return any([
        database.Post.md5_exists(md5),
        database.Post.sha256_exists(sha256),
    ])
