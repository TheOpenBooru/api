import re
from . import SearchParameters

defaults = SearchParameters()


def parseBSLs(query: str) -> SearchParameters:
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
    # match = re.match(r"(?<=(\s|^)sort:)[a-z]*(:(asc|desc))?(?=\s|$)", query)
    # if match:
    #     sort = match.string
    #     match = re.match(rf"(?<=(\s|^)sort:{sort}:)(asc|desc)?(?=\s|$)", query)
        
    # else:
    return defaults.sort, defaults.isAscending

def _parseLimit(query: str) -> int:
    match = re.match(r"(?<=limit:)[1-9][0-9]*", query)
    if match:
        return int(match.string)
    else:
        return defaults.limit


def _parseIncludeTags(query: str) -> list[str]:
    match = re.findall(r"(?<=^|\s)[a-z0-9_()]*(?=$|\s)", query)
    if match:
        return list(set(match))
    else:
        return defaults.include_tags


def _parseExcludeTags(query: str) -> list[str]:
    match = re.findall(r"(?<=(^|\s)-)[a-z_()0-9]*", query)
    if match:
        return list(set(match))
    else:
        return defaults.include_tags
