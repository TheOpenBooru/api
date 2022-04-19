from . import is_post_unique, is_post_valid, _posts_store, Post

def create(post:Post):
    """Raises:
    - KeyError: Post already exists
    - ValueError: Invalid Post Data
    """
    if not is_post_unique(post):
        raise KeyError("Post already exists")
    elif not is_post_valid(post):
        raise ValueError("Invalid Post Data")
    else:
        _posts_store[post.id] = post