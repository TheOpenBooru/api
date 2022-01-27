from dataclasses import dataclass, field

@dataclass(frozen=True)
class SearchParameters:
    include_tags: list = field(default_factory=list)
    exclude_tags: list = field(default_factory=list)
    limit: int = 64
    sort: str = "created"
    isAscending: bool = False

