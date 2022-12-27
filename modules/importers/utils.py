from modules import schemas
from cachetools import cached, Cache
from urllib.parse import urlparse
import mimetypes
import requests
import os


filename = str
async def download_url(url:str, timeout:int = 15) -> tuple[bytes, filename]:
    r = requests.get(url,timeout=timeout)
    data = r.content
    url_format = urlparse(url)
    _, ext = os.path.splitext(url_format.path)
    filename = "example" + ext
    return data, filename


def predict_media_type(url:str) -> schemas.MediaType:
    TYPE_LOOKUP = {
        ".png": schemas.MediaType.image,
        ".jpg": schemas.MediaType.image,
        ".jpeg": schemas.MediaType.image,
        ".jpef": schemas.MediaType.image,
        ".webp": schemas.MediaType.image,
        ".apng": schemas.MediaType.animation,
        ".gif": schemas.MediaType.animation,
        ".webm": schemas.MediaType.video,
        ".mp4": schemas.MediaType.video,
    }
    _,ext = os.path.splitext(url)
    if ext not in TYPE_LOOKUP:
        raise Exception(f"{ext} is not a valid media type")
    media_type = TYPE_LOOKUP[ext]
    return media_type # type: ignore


def guess_mimetype(filepath:str) -> str:
    _,ext = os.path.splitext(filepath)
    filename = 'example' + ext
    mime = _cachable_guess_mimetype(filename)
    return mime


@cached(Cache(maxsize=100))
def _cachable_guess_mimetype(filepath:str) -> str:
    full, _  = mimetypes.guess_type(filepath)
    if full == None:
        raise ValueError("Could not guess mimetype")
    else:
        return full
