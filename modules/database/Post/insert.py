from . import is_post_unique, post_collection, Post

def insert(post:Post):
    """Raises:
    - KeyError: Post already exists
    """
    if not is_post_unique(post):
        raise KeyError("Post already exists")
    else:
        document = post.dict()
        post_collection.insert_one(document=document)