import random
from modules import validate
from modules.schemas import Post
from . import User
import time

_posts_store:dict[int,Post|None] = {}

def _verify_post(post:Post):
    # Valdiate hashes
    for md5 in post.md5s:
        validate.md5(md5)
        if get(md5=md5):
            raise ValueError("Duplicate MD5")
    for sha in post.sha256s:
        validate.md5(sha)
        if get(sha256=sha):
            raise ValueError("Duplicate SHA")
    
    
    # Validate Image URLs
    validate.url(post.full.url)
    validate.url(post.preview.url) if post.preview else None
    validate.url(post.thumbnail.url) if post.thumbnail else None
    
    [validate.tag(x) for x in post.tags]
    validate.language(post.language) if post.language else None
    validate.rating(post.age_rating) if post.age_rating else None
    if post.created_at > time.time():
        raise ValueError("Created in the future")
    if post.type not in {'image','gif','video'}:
        raise ValueError("Invalid post type")

    # User's are not implemented
    # if not User.exists(post.uploader):
    #     raise ValueError("Invalid User ID")


def get_unused_id() -> int:
    return len(_posts_store) + 1


def create(post:Post):
    _verify_post(post)
    _posts_store[post.id] = post


def get(*,id:int=None,md5:str=None,sha256:str=None) -> Post | None:
    for post in _posts_store.values():
        if post == None:
            continue
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
    
    post_values = list(_posts_store.values())
    posts:list[Post] = [x for x in post_values if x != None]
    posts = list(filter(filterTags,posts))
    if isAscending:
        posts.reverse()
    posts.sort(key=lambda post: getattr(post,order))
    return posts[:limit]


def delete(id:int):
    try:
        _posts_store[id] = None
    except Exception:
        pass # Allow deleteion of non-existant posts

def clear():
    _posts_store.clear()


def increment_view(id:int):
    if id in _posts_store and _posts_store[id] != None:
        _posts_store[id].views += 1

