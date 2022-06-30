from typing import Union
from . import Post,post_collection

def get(id:int) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    return _get_by_filter({'id':id})

def getByMD5(md5:str) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    return _get_by_filter({"hashes":{"md5s":{'$elemMatch':{"$eq":md5}}}})

def getBySHA256(sha256:str) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    return _get_by_filter({"hashes":{"sha256s":{'$elemMatch':{"$eq":sha256}}}})

def _get_by_filter(filter: dict):
    document = post_collection.find_one(filter)
    if document == None:
        raise KeyError("Could not find post")
    else:
        post = Post.parse_obj(document)
        return post