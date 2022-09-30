from . import iter_over_posts, parsing
from .. import Importer, utils
from modules import settings, schemas, database, posts
from modules.importers.classes import ImportFailure
from typing import Union
from itertools import islice
from tqdm import tqdm
from pathlib import Path
import logging
import requests


class E621(Importer):
    enabled = settings.IMPORTER_E621_ENABLED
    time_between_runs = settings.IMPORTER_E621_RETRY_AFTER
    def __init__(self):
        requests.get("https://e621.net", timeout=2)


    async def load(self, limit:Union[int, None] = None):
        progress = tqdm(
            desc="Importing From E621 Dump",
            unit=" post",
            iterable=islice(iter_over_posts(), limit),
            total=limit or guess_post_count(),
        )

        for data in progress:
            try:
                await load_post(data)
            except ImportFailure:
                pass
            except Exception as e:
                logging.exception(e)


async def load_post(data:dict):
    try:
        md5 = bytes.fromhex(data['file']['md5'])
        post = database.Post.md5_get(md5)
    except KeyError:
        await import_post(data)
    else:
        await update_post(post, data)

def guess_post_count() -> int:
    path = Path(settings.IMPORTER_E621_DUMP)
    stats = path.stat()
    size = stats.st_size
    AVG_POST_SIZE = 1682
    return size // AVG_POST_SIZE


async def update_post(post:schemas.Post, data:dict):
    modified_post = post.copy()
    
    modified_post.upvotes = parsing.get_upvotes(data)
    modified_post.downvotes = parsing.get_downvotes(data)
    modified_post.source = parsing.get_source(data)
    modified_post.tags = parsing.get_tags(data, post.full.type)
    modified_post.source = parsing.get_source(data)

    if modified_post != post:
        database.Post.update(post.id, modified_post)



async def import_post(data:dict):
    full = parsing.construct_image(data['file'])
    preview = parsing.construct_image(data['sample'])
    thumbnail = parsing.construct_image(data['preview'])
    if full == None or thumbnail == None:
        raise ImportFailure("Failed to Generate Images from E621 Post")

    post = schemas.Post(
        id=database.Post.generate_id(),
        created_at=parsing.get_date(data['created_at']),
        media_type=utils.predict_media_type(data['file']['url']), # type: ignore
        full=full,
        preview=preview,
        thumbnail=thumbnail,
        tags=parsing.get_tags(data, full.type),
        source=parsing.get_source(data),
        upvotes=data['score']['up'],
        downvotes=data['score']['down'],
        hashes=schemas.Hashes(md5s=[bytes.fromhex(data['file']['md5'])]),
        rating=schemas.Rating.explicit,
    )
    await posts.insert(post, validate=False)

