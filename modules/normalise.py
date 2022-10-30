from typing import Union
from modules import validate
from functools import cache
import string

def normalise_tags(tags: list[str]) -> list[str]:
    tags = [normalise_tag(tag) for tag in tags]
    filter_iterable = filter(validate.tag, tags)
    tags = list(set(list(filter_iterable)))
    return tags


_VALID_TAG_CHARS = set(string.ascii_lowercase + string.digits + '_()')

@cache
def normalise_tag(tag:str, *, possibly_namespaced:bool = False) -> str:
    if possibly_namespaced:
        sections = tag.split(':')
        if len(sections) == 2:
            _,tag = sections

    tag = (
        tag
        .lower()
        .strip('\n')
        .replace(' ','_')
    )
    filter_func = lambda chr: chr in _VALID_TAG_CHARS
    filtered_chars = list(filter(filter_func, tag))
    tag = ''.join(filtered_chars)
    
    return tag
