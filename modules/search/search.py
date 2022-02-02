from dataclasses import dataclass, field
from modules import types
from modules.database import Post

@dataclass()
class SearchParameters:
    include_tags: list = field(default_factory=list)
    exclude_tags: list = field(default_factory=list)
    limit: int = 64
    sort: str = "created"
    isAscending: bool = False

def searchPosts(params:SearchParameters) -> list[types.Post]:
    posts = Post.search(
        limit=params.limit,
        order=params.sort,
        isAscending=params.isAscending,
        hasTags=params.include_tags,
        excludeTags=params.exclude_tags,
    )
    return [post.to_pydantic() for post in posts]
