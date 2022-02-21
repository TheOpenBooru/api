from dataclasses import dataclass, field
from modules import schemas,settings
from modules.database import Post

@dataclass()
class SearchParameters:
    include_tags: list = field(default_factory=list)
    exclude_tags: list = field(default_factory=list)
    limit: int = 64
    sort: str = "created_at"
    isAscending: bool = False

def searchPosts(params:SearchParameters) -> list[schemas.Post]:
    max_limit = settings.get('settings.search.max_limit')
    limit = params.limit
    limit = max(0,limit) # prevent negative limits
    limit = min(max_limit,limit) # Prevent limits above maximum
    posts = Post.search(
        limit=limit,
        order=params.sort,
        isAscending=params.isAscending,
        hasTags=params.include_tags,
        excludeTags=params.exclude_tags,
    )
    return posts
