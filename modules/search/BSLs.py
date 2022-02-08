import re
from . import SearchParameters

defaults = SearchParameters()


def parseBSLs(query: str) -> SearchParameters:
    return SearchParameters()
    limit = _parseLimit(query)
    sort,order = _parseSort(query)
    includes = _parseIncludeTags(query)
    excludes = _parseExcludeTags(query)
    return SearchParameters(
        limit=limit,
        sort=sort,
        isAscending=order,
        include_tags=includes,
        exclude_tags=excludes,
    )


def _parseSort(query: str) -> tuple[str, bool]:
    return defaults.sort, defaults.isAscending

def _parseLimit(query: str) -> int:
    return defaults.limit


def _parseIncludeTags(query: str) -> list[str]:
    return defaults.include_tags
""

def _parseExcludeTags(query: str) -> list[str]:
    return defaults.include_tags
