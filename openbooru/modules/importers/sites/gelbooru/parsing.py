from openbooru.modules.importers import utils
from openbooru.modules import schemas, normalise
from typing import Callable
from datetime import datetime

def construct_image(url:str, width:str, height:str):
    return schemas.Image(
        url=url,
        width=int(width),
        height=int(height),
        mimetype=utils.guess_mimetype(url),
        type=utils.predict_media_type(url) # type: ignore
    )


def get_images(post:dict) -> tuple[schemas.Image,schemas.Image,schemas.Image]:
    full = construct_image(
        url=post['file_url'],
        height=post['height'],
        width=post['width'],
    )
    preview = construct_image(
        url=post['sample_url'],
        height=post['sample_height'],
        width=post['sample_width'],
    )
    thumbnail = construct_image(
        url=post['preview_url'],
        height=post['preview_height'],
        width=post['preview_width'],
    )
    return full, preview, thumbnail


DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"
def get_date(post:dict) -> int:
    date_string = post["created_at"]
    date = datetime.strptime(date_string,DATE_FORMAT)
    timestamp = int(date.timestamp())
    return timestamp


def get_md5(post:dict) -> bytes:
    return bytes.fromhex(post["md5"])


def get_rating(post:dict) -> schemas.Rating:
    if post["rating"] == "e":
        return schemas.Rating.explicit
    elif post["rating"] == "m":
        return schemas.Rating.mature
    elif post["rating"] == "s":
        return schemas.Rating.safe
    else:
        return schemas.Rating.unrated


def get_hashes(post:dict) -> schemas.Hashes:
    return schemas.Hashes(
        md5s=[get_md5(post)]
    )


def get_sources(hostname: str) -> Callable[[dict],list[str]]:
    def inner(post: dict) -> list[str]:
        sources = []
        sources.append(f"https://{hostname}/index.php?page=post&s=view&id={post['id']}")
        if post["source"]:
            sources.append(post["source"])
        
        return sources
    
    return inner


def get_tags(post:dict):
    tags = post["tags"].split(" ")
    tags.append("rule34")
    return normalise.normalise_tags(tags)


def get_score(post: dict):
    return int(post["score"] or "0")
