from .. import utils
from modules import schemas
from datetime import datetime


def get_score(post:dict) -> int:
    return int(post['score'] or "0")


def get_tags(post:dict) -> list[str]:
    tag_string = post['tags']
    tags = tag_string.split(' ')
    return utils.normalise_tags(tags)


def get_source(post:dict) -> str:
    if post['source']:
        return post['source']
    else:
        return f"https://safebooru.org/index.php?page=post&s=view&id={post['id']}"


def get_hashes(post:dict) -> schemas.Hashes:
    md5 = post['md5']
    return schemas.Hashes(md5s=[md5])


def get_date(dateString:str) -> int:
    format = "%a %b %d %H:%M:%S %z %Y"
    date = datetime.strptime(dateString,format)
    timestamp = int(date.timestamp())
    return timestamp


def construct_images(attrs:dict) -> tuple[schemas.Image,schemas.Image,schemas.Image]:
    full = schemas.Image(
        url=attrs['file_url'],
        width=attrs['width'],
        height=attrs['height'],
        mimetype=utils.guess_mimetype(attrs['file_url']),
    )
    preview = schemas.Image(
        url=attrs['sample_url'],
        width=attrs['sample_width'],
        height=attrs['sample_height'],
        mimetype=utils.guess_mimetype(attrs['sample_url']),
    )
    thumbnail = schemas.Image(
        url=attrs['preview_url'],
        width=attrs['preview_width'],
        height=attrs['preview_height'],
        mimetype=utils.guess_mimetype(attrs['preview_url']),
    )
    return full, preview, thumbnail
