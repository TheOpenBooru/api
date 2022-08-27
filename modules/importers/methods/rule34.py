from functools import cache
from . import Importer, ImportFailure, utils
from modules import settings, schemas, database
from tqdm import tqdm
from datetime import datetime
from pathlib import Path
from typing import Union
import ijson


class Rule34(Importer):
    enabled = settings.IMPORTER_RULE34_ENABLED
    def __init__(self):
        self.functional = Path(settings.IMPORTER_RULE34_DUMP).exists()


    async def load(self, limit:Union[int, None] = None):
        posts = iter_over_posts()
        progress = tqdm(
            iterable=posts,
            desc="Importing From Rule34 Dump",
            unit=" post",
            total=guess_post_count(),
        )
        post_count = 0
        for post in progress:
            post_count += 1
            if limit and post_count > limit:
                return
            
            try:
                post = await post_from_dict(post)
                database.Post.insert(post)
            except Exception as e:
                continue


def guess_post_count() -> int:
    path = Path(settings.IMPORTER_E621_DUMP)
    stats = path.stat()
    size = stats.st_size
    AVG_POST_SIZE = 1057
    return size // AVG_POST_SIZE


def iter_over_posts():
    with open(settings.IMPORTER_RULE34_DUMP) as f:
        parser = ijson.parse(f)
        post = {}
        key = ""
        for prefix, event, value in parser:
            if event == "start_map":
                post = {}
            elif event == "map_key":
                key = value
            elif event == "string":
                post[key] = value
            elif event == "end_map":
                yield post


async def post_from_dict(data:dict) -> schemas.Post:
    if database.Post.md5_exists(data['md5']):
        raise ImportFailure("Post Already Exists")
    
    full,preview,thumbnail = construct_images(data)
    post = schemas.Post(
        id=database.Post.generate_id(),
        created_at=get_date(data),
        upvotes=get_score(data["score"]),
        tags=get_tags(data) + ["rule34xxx", full.type],
        source=get_source(data),
        media_type=utils.predict_media_type(data['file_url']), # type: ignore
        hashes=get_hashes(data),
        full=full,
        preview=preview,
        thumbnail=thumbnail,
    )
    return post


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


def get_hashes(post:dict):
    return schemas.Hashes(
        md5s=[post["md5"]]
    )


def get_source(post:dict) -> str:
    if post['source']:
        return post['source']
    else:
        return f"https://rule34.xxx/index.php?page=post&s=view&id={post['id']}"


def get_tags(post:dict):
    tag_string = post['tags']
    tags = tag_string.split(' ')
    tags = utils.normalise_tags(tags)
    return tags


@cache
def get_score(score:str):
    return int(score or "0")


def generate_proxy_url(url:str):
    template =settings.IMPORTER_RULE34_PROXY_FORMAT
    return template.format(url=url)
