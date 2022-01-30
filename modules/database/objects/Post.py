from ..types import Post
from . import Image
import time

_posts = {}

def create(
    creator:int,
    fullID:int,prevID:int,thumbID:int,
    md5:str,sha256:str,
    language:str,source:str,rating:str,
    type:str,sound:bool
    ) -> int:
    post = Post(
        id=len(_posts),
        creator=creator,
        created_at=int(time.time()),
        md5=[md5],sha256=[sha256],
        language=language,source=source,rating=rating,
        type=type,sound=sound,
        views=0,upvotes=0,downvotes=0,
        full=Image.get(id=fullID),preview=Image.get(id=prevID),thumbnail=Image.get(id=thumbID),
        tags=[],comments=[]
    )
    _posts[post.id] = post
    return post.id


def get(id:int) -> Post:
    return _posts[id]


def search(limit:int=64,order:str='created_at') -> list[Post]:
    """Raises:
        ValueError: Invalid Ordering
    """
    return _posts[:100]


def set(id:int,source:str=None,rating:str=None,tags:list[str]=None):
    post = get(id)
    post.source = source or post.source
    post.rating = rating or post.rating
    post.tags = tags or post.tags


def delete(id:int):
    _posts.pop(id)
