from .parsing import get_date, get_hashes, get_source, get_score, get_tags, construct_images
from .iterable import safebooru_search
from .. import utils, Importer
from modules import settings, schemas, database, posts
from typing import Union
from tqdm import tqdm
import requests


class Safebooru(Importer):
    enabled = settings.IMPORTER_SAFEBOORU_ENABLED
    time_between_runs = settings.IMPORTER_SAFEBOORU_RETRY_AFTER
    def __init__(self):
        requests.get("https://safebooru.org/",timeout=2)


    async def load(self, limit:Union[int, None] = settings.IMPORTER_SAFEBOORU_LIMIT):
        searches = settings.IMPORTER_SAFEBOORU_SEARCHES
        
        posts = []
        for search in searches:
            new_posts = await safebooru_search(search,limit)
            posts.extend(new_posts)
            if limit and len(posts) > limit:
                break

        for i, data in enumerate(tqdm(posts, desc="Importing From Safebooru")):
            if limit and i >= limit:
                return

            try:
                md5 = bytes.fromhex(data['md5'])
                post = database.Post.getByMD5(md5)
            except KeyError:
                await insert_post(data)
            else:
                await update_post(data, post)


async def insert_post(data:dict):
    full,preview,thumbnail = construct_images(data)
    post = schemas.Post(
        id=database.Post.generate_id(),
        created_at=get_date(data['created_at']),
        upvotes=get_score(data),
        tags=get_tags(data),
        source=get_source(data),
        media_type=utils.predict_media_type(data['file_url']), # type: ignore
        hashes=get_hashes(data),
        full=full,
        preview=preview,
        thumbnail=thumbnail,
    )
    database.Post.insert(post)


async def update_post(data:dict, post:schemas.Post):
    new_post = post.copy()

    new_post.upvotes = get_score(data)
    new_post.source = get_source(data)
    new_post.tags = get_tags(data)

    if post != new_post:
        database.Post.update(post.id, new_post)