from . import _posts_store

def increment_view(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if id not in _posts_store:
        raise KeyError("Post not found")
    
    _posts_store[id].views += 1 # type: ignore
