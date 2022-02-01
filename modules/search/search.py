from dataclasses import dataclass, field
from endpoints.types import Post

@dataclass(frozen=True)
class SearchParameters:
    include_tags: list = field(default_factory=list)
    exclude_tags: list = field(default_factory=list)
    limit: int = 64
    sort: str = "created"
    isAscending: bool = False

def searchPosts(params:SearchParameters) -> list[Post]:
    ...
