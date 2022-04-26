from modules import validate
import re
import string

_VALID_CHARS = string.ascii_lowercase + string.digits + '_'

def normalise_tag(tag:str) -> str:
    tag = tag.strip('\n')
    tag = tag.replace(' ','_')
    tag_chars = list(tag)
    filter_func = lambda char:re.match(validate.TAG_REGEX,char)
    filtered_chars = list(filter(filter_func,tag_chars))
    tag = ''.join(filtered_chars)

    if validate.tag(tag):
        return tag
    else:
        return ""
