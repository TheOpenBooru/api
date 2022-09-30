from . import generate, exists_hash, insert, PostExistsException
from modules import database, settings
from modules.tags import generate_ai_tags
import hashlib
import mimetypes
from typing import Union


async def create(data:bytes,filename:str,
        use_ai_tags:bool=settings.TAGS_TAGGING_SERVICE_ENABLED,
        uploader_id:Union[int,None] = None,
        additional_tags:Union[list[str],None] = None,
        source:Union[str,None] = None,
        rating:Union[str,None] = None,
        ):
    if exists_hash(data):
        raise PostExistsException
    
    post = await generate(data,filename,use_ai_tags,uploader_id,additional_tags,source,rating)
    await insert(post, validate=True)
    return post
