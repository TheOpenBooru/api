from . import Post, _posts_store

def get_unused_id() -> int:
    return len(_posts_store) + 1

def all() -> list[Post]:
    valid_posts = [x for x in _posts_store.values() if x != None]
    return valid_posts

def clear():
    _posts_store.clear()