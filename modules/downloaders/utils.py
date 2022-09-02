from modules.normalisation import normalise_tag, normalise_tags
from cachetools import cached, Cache
import string
import mimetypes
import requests
import os
import bs4


filename = str
def download_url(url:str, timeout:int = 15) -> tuple[bytes, filename]:
    r = requests.get(url,timeout=timeout)
    data = r.content
    _, ext = os.path.splitext(url)
    filename = "example" + ext
    return data, filename


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


@cached(cache=Cache(maxsize=10_000))
def _cachable_guess_mimetype(filepath:str) -> str:
    full, _  = mimetypes.guess_type(filepath)
    if full == None:
        raise ValueError("Could not guess mimetype")
    else:
        return full
