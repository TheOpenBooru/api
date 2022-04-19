from . import _posts_store

def delete(id:int):
    if id in _posts_store:
        _posts_store[id].deleted = True

def restore(id:int):
    """Raises:
    - KeyError: Post not found
    """
    if id not in _posts_store:
        raise KeyError("Post not found")
    
    _posts_store[id].deleted = False
