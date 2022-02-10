import re
import logging
from . import SearchParameters

defaults = SearchParameters()


def parseBSLs(query: str) -> SearchParameters:
    limit = defaults.limit
    includes = []
    excludes = []
    sort,order = defaults.sort, defaults.isAscending
    for tag in query.split(' '):
        limit = _parseLimit(tag) or limit
        sort,order = _parseSort(tag) or (sort,order)
        if _parseIncludeTags(tag):
            includes.append(tag)
        if _parseExcludeTags(tag):
            excludes.append(tag)
    config = SearchParameters(
        limit=limit,
        sort=sort,
        isAscending=order,
        include_tags=includes,
        exclude_tags=excludes,
    )
    logging.debug(f"Parsed BSLs: '{query}' to {str(config)}")
    return config


def _parseSort(query: str) -> tuple[str, bool]|None:
    return defaults.sort, defaults.isAscending

def _parseLimit(query: str) -> int|None:
    match = re.match('^limit:[0-9]+$',query)
    if match:
        return int(match.string[6:])

def _parseIncludeTags(query: str) -> str|None:
    match = re.match(r'^(?<![-:])\b[a-z0-9_()]+\b(?!:)$',query)
    if match:
        return match.string

def _parseExcludeTags(query: str) -> str|None:
    match = re.match(r'^(?<=-)[a-z0-9_()]+(?!:)$',query)
    if match:
        return match.string