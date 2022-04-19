from . import Post,_posts_store

def update(id:int,new_version:Post):
    """Raises:
    - KeyError: Post not found
    """
    if id not in _posts_store:
        raise KeyError("Post not found")
    _posts_store[id] = new_version