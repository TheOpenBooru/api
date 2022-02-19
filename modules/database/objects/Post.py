from modules import validate
from ..types import Post
from . import User
import time

_posts_store:dict[int,Post] = {}

def _verify_post(post:Post):
    # Valdiate hashes
    [validate.md5(x) for x in post.md5s]
    [validate.sha256(x) for x in post.sha256s]
    # Validate Image URLs
    validate.url(post.full.url)
    validate.url(post.preview.url) if post.preview else None
    validate.url(post.thumbnail.url) if post.thumbnail else None
    
    validate.language(post.language) if post.language else None
    validate.rating(post.rating) if post.rating else None
    if int(time.time() + 1) < post.created_at:
        raise ValueError("Created in the future")
    if post.type not in {'image','gif','video'}:
        raise ValueError("Invalid post type")
    if not User.exists(post.creator):
        raise ValueError("Invalid User ID")

def create(post:Post):
    _verify_post(post)
    post.id = len(_posts_store) + 1
    _posts_store[post.id] = post


def get(*,id:int=None,md5:str=None,sha256:str=None) -> Post | None:
    for post in _posts_store.values():
        if ((id and post.id == id) or
            (md5 and md5 in post.md5s ) or
            (sha256 and sha256 in post.sha256s)):
            return post
    return None

def update(id:int,new_version:Post):
    """Raises:
    - KeyError: Post not found
    """
    if id not in _posts_store:
        raise KeyError("Post not found")
    _posts_store[id] = new_version


def delete(id:int):
    try:
        _posts_store.pop(id)
    except Exception:
        pass # Allow deleteion of non-existant posts

def search(limit:int=64,order:str='created_at',isAscending:bool=False,
           hasTags:list[str]=None,excludeTags:list[str]=None) -> list[Post]:
    """Raises:
    - ValueError: Invalid Ordering
    """
    hasTags = hasTags or []
    excludeTags = excludeTags or []
    
    def filterTags(post:Post) -> bool:
        if hasTags:
            for tag in hasTags:
                return tag in post.tags
        if excludeTags:
            for tag in excludeTags:
                return tag not in post.tags
        return True
    
    posts:list[Post] = list(_posts_store.values())
    posts = list(filter(filterTags,posts))
    if isAscending:
        posts.reverse()
    posts.sort(key=lambda post: getattr(post,order))
    return posts[:limit]
