from . import is_post_unique, post_collection, Post
import pymongo.errors

def insert(post:Post):
    """Raises:
    - KeyError: Post already exists
    """
    document = post.dict()
    try:
        post_collection.insert_one(document=document)
    except pymongo.errors.DuplicateKeyError:
        raise KeyError("Post already exists")