from modules import validate
from functools import cache
import string

def normalise_tags(tags:list[str]) -> list[str]:
    tags = [normalise_tag(tag) for tag in tags]
    tags = list(filter(validate.tag, tags))
    tags = list(set(tags))
    tags.sort()
    return tags


_VALID_TAG_CHARS = string.ascii_lowercase + string.digits + '_()'

@cache
def normalise_tag(tag:str, *, possibly_namespaced:bool = True) -> str:
    if possibly_namespaced:
        sections = tag.split(':')
        if len(sections) == 2:
            _,tag = sections

    tag = tag.lower()
    tag = tag.strip('\n')
    tag = tag.replace(' ','_')
    tag_chars = list(tag)
    
    filter_func = lambda chr: chr in _VALID_TAG_CHARS
    filtered_chars = list(filter(filter_func,tag_chars))
    tag = ''.join(filtered_chars)
    
    return tag
