from ..types import Post,Image
import time

_posts = {}

def create(
    creator:int,
    full:Image,preview:Image,thumbnail:Image,
    md5:str,sha256:str,
    type:str,sound:bool
    ) -> int:
    post = Post(
        id=len(_posts),creator=creator,
        created_at=int(time.time()),
        md5=[md5],sha256=[sha256],
        full=full,preview=preview,thumbnail=thumbnail,
        type=type,sound=sound,
        views=0,upvotes=0,downvotes=0,
        language="",source="",rating="",
        tags=[],comments=[]
    )
    _posts[post.id] = post
    return post.id


def get(id:int) -> Post:
    return _posts[id]


def search(limit:int=64,order:str='created_at',isAscending:bool=False,
           hasTags:list[str]=[],excludeTags:list[str]=[]) -> list[Post]:
    """Raises:
        ValueError: Invalid Ordering
    """
    posts:list[Post] = list(_posts.values())
    posts[0].tags
    def filterTags(post:Post) -> bool:
        for tag in hasTags:
            if tag not in post.tags:
                return False
        for tag in excludeTags:
            if tag in post.tags:
                return False
        return True
    posts = list(filter(filterTags,posts))
    if isAscending:
        posts.reverse()
    posts.sort(key=lambda post: getattr(post,order))
    return posts[:limit]


def set(id:int,source:str=None,rating:str=None,tags:list[str]=None):
    post = get(id)
    post.source = source or post.source
    post.rating = rating or post.rating
    post.tags = tags or post.tags


def delete(id:int):
    _posts.pop(id)
