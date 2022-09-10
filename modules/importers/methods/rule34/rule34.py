from . import iter_over_posts, guess_post_count, parsing
from .. import Importer, ImportFailure, utils
from modules import settings, schemas, database
from tqdm.asyncio import tqdm
from typing import Union
from itertools import islice


class Rule34(Importer):
    enabled = settings.IMPORTER_RULE34_ENABLED
    time_between_runs = settings.IMPORTER_RULE34_RETRY_AFTER


    async def load(self, limit:Union[int, None] = None):
        progress = tqdm(
            iterable=iter_over_posts(limit),
            desc="Importing From Rule34 Dump",
            unit=" post",
            total=limit or guess_post_count(),
        )
        async for post in progress:
            try:
                await load_post(post)
            except ImportFailure:
                continue



async def load_post(data:dict):
    try:
        post = database.Post.getByMD5(parsing.get_md5(data))
    except KeyError:
        await import_post(data)
    else:
        await update_post(post, data)


async def import_post(data:dict):
    full,preview,thumbnail = parsing.construct_images(data)
    post = schemas.Post(
        id=database.Post.generate_id(),
        created_at=parsing.get_date(data),
        upvotes=parsing.get_score(data["score"]),
        tags=parsing.get_tags(data, full.type),
        source=parsing.get_source(data),
        media_type=utils.predict_media_type(data['file_url']),
        hashes=parsing.get_hashes(data),
        rating=schemas.Rating.explicit,
        full=full,
        preview=preview,
        thumbnail=thumbnail,
    )
    database.Post.insert(post)


async def update_post(post:schemas.Post, data:dict):
    modified_post = post.copy()
    
    modified_post.upvotes = parsing.get_score(data["score"])
    modified_post.source = parsing.get_source(data)
    modified_post.tags = parsing.get_tags(data, post.full.type)

    if modified_post != post:
        database.Post.update(post.id, modified_post)

