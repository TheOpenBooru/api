import re as _re
import logging as _logging
from . import SearchParameters as _SearchParameters

defaults = _SearchParameters()


def parseBSLs(query: str) -> _SearchParameters:
    tags = [tag.strip('\n\r ') for tag in query.split(' ')]

    params = _SearchParameters()
    params.sort, params.isAscending = _parseSort(tags)
    params.limit = _parseLimit(tags)
    params.include_tags = _getIncludeTag(tags)
    params.exclude_tags = _getExcludeTag(tags)
    
    _logging.debug(f"Parsed BSLs: '{query}' to {params}")
    return params


def _parseSort(tags: list[str]) -> tuple[str, bool]:
    sort = defaults.sort
    isAscending = defaults.isAscending
    for tag in tags:
        sort_match = _re.match(r"^sort:[a-z]+$",tag)
        if sort_match:
            sort = sort_match.string[5:] # remove 'sort:'
            break 
    return sort, isAscending

def _parseLimit(tags: list[str]) -> int:
    limit = defaults.limit
    for tag in tags:
        match = _re.match(r'limit:[1-9][0-9]*',tag)
        if match:
            limit = int(match.string[6:]) # remove 'limit:'
            break
    return limit

def _getIncludeTag(tags: list[str]) -> list[str]:
    include_tags = set()
    for tag in tags:
        match = _re.match(r'^(?<![-:])\b[a-z0-9_()]+\b(?!:)$',tag)
        if match:
            include_tags.add(tag)
    return list(include_tags)

def _getExcludeTag(tags: list[str]) -> list[str]:
    exclude_tags = set()
    for tag in tags:
        match = _re.match(r'^-[a-z0-9_()]+(?!:)$',tag)
        if match:
            tag = tag[1:] # remove '-'
            exclude_tags.add(tag)
    return list(exclude_tags)