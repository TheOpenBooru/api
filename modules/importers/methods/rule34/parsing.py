from .. import utils
from modules import schemas, settings
from datetime import datetime
from functools import cache

def construct_image(url:str, width:str, height:str):
    return schemas.Image(
        url=generate_proxy_url(url),
        width=int(width),
        height=int(height),
        mimetype=utils.guess_mimetype(url),
        type=utils.predict_media_type(url) # type: ignore
    )


def construct_images(post:dict) -> tuple[schemas.Image,schemas.Image,schemas.Image]:
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


def get_hashes(post:dict) -> schemas.Hashes:
    return schemas.Hashes(
        md5s=[get_md5(post)]
    )


def get_source(post:dict) -> str:
    if post['source']:
        return post['source']
    else:
        return f"https://rule34.xxx/index.php?page=post&s=view&id={post['id']}"


def get_tags(post:dict, type:str):
    tag_string:str = post['tags']
    tags = tag_string.split(' ')
    tags.append(type)
    tags.append("rule34xxx")
    tags = utils.normalise_tags(tags)
    return tags


@cache
def get_score(score:str):
    return int(score or "0")


def generate_proxy_url(url:str):
    template =settings.IMPORTER_RULE34_PROXY_FORMAT
    return template.format(url=url)
