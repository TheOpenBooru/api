from . import post_collection, Post, encode_post
import pymongo.errors

def insert(post:Post):
    """Raises:
    - KeyError: Post already exists
    """
    document = encode_post(post)
    try:
        post_collection.insert_one(document=document)
    except pymongo.errors.DuplicateKeyError:
        raise KeyError("Post already exists")

def insertMany(posts: list[Post]):
    """Raises:
    - KeyError: Post already exists
    """
    documents = [encode_post(post) for post in posts]
    try:
        post_collection.insert_many(documents)
    except pymongo.errors.DuplicateKeyError:
        raise KeyError("Post already exists")