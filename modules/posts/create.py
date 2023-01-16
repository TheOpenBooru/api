from . import generate, exists_data, insert, PostExistsException
from modules import database, settings
from modules.tags import generate_ai_tags
import hashlib
import mimetypes
from typing import Union


async def create(data:bytes, filename:str, uploader_id: None|int = None):
    if exists_data(data):
        raise PostExistsException
    
    post = await generate(data, filename, uploader_id)
    await insert(post, validate=True)
    return post
