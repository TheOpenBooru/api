from modules import validate
import string

_VALID_CHARS = string.ascii_lowercase + string.digits + '_'

def normalise_tags(tags:list[str]) -> list[str]:
    if " " in tags:
        tags.remove(" ")

    tags = [normalise_tag(tag) for tag in tags]
    tags = list(filter(validate.tag,tags))
    tags = list(set(tags))
    return tags

def normalise_tag(tag:str) -> str:
    sections = tag.split(':')
    if len(sections) == 2:
        tag = sections[1]
    
    tag = tag.strip('\n')
    tag = tag.replace(' ','_')
    tag_chars = list(tag)
    
    filter_func = lambda chr: chr in _VALID_CHARS
    filtered_chars = list(filter(filter_func,tag_chars))
    tag = ''.join(filtered_chars)
    
    return tag
