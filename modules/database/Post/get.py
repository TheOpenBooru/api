from typing import Union
from . import Post, post_collection, parse_doc


def get(id:int) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    if (id) > 2**63:
        raise KeyError("Post ID Too Large")
    return _get_by_filter({'id':id})


def md5_get(md5:bytes) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    return _get_by_filter({"hashes.md5s":{'$elemMatch':{"$eq":md5}}})


def sha256_get(sha256:bytes) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    return _get_by_filter({"hashes.sha256s":{'$elemMatch':{"$eq":sha256}}})


def phash_get(phash:bytes) -> Post:
    """Raises
    - KeyError: Could not find post
    """
    return _get_by_filter({"hashes.phashes":{'$elemMatch':{"$eq":phash}}})


def _get_by_filter(filter: dict):
    document = post_collection.find_one(filter)
    if document == None:
        raise KeyError("Could not find post")
    else:
        return parse_doc(document)
