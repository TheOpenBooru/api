from dataclasses import dataclass, field
from modules import types
from modules.database import Post

@dataclass(frozen=True)
class SearchParameters:
    include_tags: list = field(default_factory=list)
    exclude_tags: list = field(default_factory=list)
    limit: int = 64
    sort: str = "created"
    isAscending: bool = False

def searchPosts(params:SearchParameters) -> list[types.Post]:
    posts = Post.search(params.limit,params.sort,params.isAscending)
    return [post.to_pydantic() for post in posts]
