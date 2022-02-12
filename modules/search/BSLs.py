import re as _re
import logging as _logging
from . import SearchParameters

defaults = SearchParameters()


def parseBSLs(query: str) -> SearchParameters:
    limit = defaults.limit
    includes = set()
    excludes = set()
    sort,order = defaults.sort, defaults.isAscending
    for tag in query.split(' '):
        tag = tag.strip('\n\r ')
        limit = _parseLimit(tag) or limit
        sort,order = _parseSort(tag) or (sort,order)
        if _isIncludeTag(tag):
            includes.add(tag)
        if _isExcludeTag(tag):
            tag = tag[1:] # Remove the -
            excludes.add(tag)
    config = SearchParameters(
        limit=limit,
        sort=sort,
        isAscending=order,
        include_tags=list(includes),
        exclude_tags=list(excludes),
    )
    _logging.debug(f"Parsed BSLs: '{query}' to {config}")
    return config


def _parseSort(query: str) -> tuple[str, bool]|None:
    return defaults.sort, defaults.isAscending

def _parseLimit(query: str) -> int|None:
    match = _re.match(r'limit:[1-9][0-9]*',query)
    if match:
        limitInterger = match.string[6:]
        return int(limitInterger)

def _isIncludeTag(query: str) -> bool:
    match = _re.match(r'^(?<![-:])\b[a-z0-9_()]+\b(?!:)$',query)
    return bool(match)

def _isExcludeTag(query: str) -> bool:
    match = _re.match(r'^-[a-z0-9_()]+(?!:)$',query)
    return bool(match)