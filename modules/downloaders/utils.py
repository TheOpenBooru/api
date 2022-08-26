from functools import cache
from modules import validate, schemas
import string
import mimetypes
import requests
import os
import bs4


_VALID_CHARS = string.ascii_lowercase + string.digits + '_()'

filename = str
def download_url(url:str, timeout:int = 15) -> tuple[bytes, filename]:
    r = requests.get(url,timeout=timeout)
    data = r.content
    _, ext = os.path.splitext(url)
    filename = "example" + ext
    return data, filename


def normalise_tags(tags:list[str]) -> list[str]:
    tags = [normalise_tag(tag) for tag in tags]
    tags = list(filter(validate.tag, tags))
    tags = list(set(tags))
    return tags


@cache
def normalise_tag(tag:str,*, possibly_namespaced:bool = True) -> str:
    if possibly_namespaced:
        sections = tag.split(':')
        if len(sections) == 2:
            _,tag = sections

    tag = tag.lower()
    tag = tag.strip('\n')
    tag = tag.replace(' ','_')
    tag_chars = list(tag)
    
    filter_func = lambda chr: chr in _VALID_CHARS
    filtered_chars = list(filter(filter_func,tag_chars))
    tag = ''.join(filtered_chars)
    
    return tag


def predict_media_type(url:str) -> str:
    TYPE_LOOKUP = {
        ".mp4":"video",
        ".webm":"video",
        ".webp":"image",
        ".png":"image",
        ".jpg":"image",
        ".jpeg":"image",
        ".gif":"animation",
    }
    _,ext = os.path.splitext(url)
    if ext not in TYPE_LOOKUP:
        raise Exception(f"{ext} is not a valid media type")
    media_type = TYPE_LOOKUP[ext]
    return media_type # type: ignore


def guess_mimetype(filepath:str) -> str:
    _,ext = os.path.splitext(filepath)
    filename = 'example' + ext
    return _cachable_guess_mimetype(filename)


@cache
def _cachable_guess_mimetype(filepath:str) -> str:
    full, _  = mimetypes.guess_type(filepath)
    if full == None:
        raise ValueError("Could not guess mimetype")
    else:
        return full
