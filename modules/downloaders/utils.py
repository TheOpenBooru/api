from modules import schemas
from modules.normalisation import normalise_tag, normalise_tags
from cachetools import cached, Cache
import mimetypes
import requests
import os


filename = str
def download_url(url:str, timeout:int = 15) -> tuple[bytes, filename]:
    r = requests.get(url,timeout=timeout)
    data = r.content
    _, ext = os.path.splitext(url)
    filename = "example" + ext
    return data, filename


def predict_media_type(url:str) -> schemas.MediaType:
    TYPE_LOOKUP = {
        ".mp4": schemas.MediaType.video,
        ".webm": schemas.MediaType.video,
        ".webp": schemas.MediaType.image,
        ".png": schemas.MediaType.image,
        ".jpg": schemas.MediaType.image,
        ".jpeg": schemas.MediaType.image,
        ".gif": schemas.MediaType.animation,
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
