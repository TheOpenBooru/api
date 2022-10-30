from modules import database, posts, schemas
from modules.importers import utils
from modules.schemas import GenericMedia, Image
from typing import Callable, TypeVar, AsyncIterable, Iterable
import inspect
import time
import logging


V = TypeVar("V")
async def run_importer(
        iterable:AsyncIterable[V]|Iterable[V],
        limit: int|None,
        get_hashes: Callable[[V], schemas.Hashes],
        get_images: Callable[[V], tuple[GenericMedia, GenericMedia|None, Image]],
        get_tags: Callable[[V], list[str]] = lambda _:[],
        get_created_at: Callable[[V], float] = lambda _: time.time(),
        get_upvotes: Callable[[V], int] = lambda _: 0,
        get_downvotes: Callable[[V], int] = lambda _: 0,
        get_sources: Callable[[V], list[str]] = lambda _:[],
        get_rating: Callable[[V], schemas.Rating] = lambda _:schemas.Rating.unrated,
    ):
    async def import_post(data: V):
        full,preview,thumbnail = get_images(data)
        post = schemas.Post(
            id=database.Post.generate_id(),
            full=full,
            preview=preview,
            thumbnail=thumbnail,
            hashes=get_hashes(data),
            type=utils.predict_media_type(full.url),
            created_at=get_created_at(data),
            tags=get_tags(data),
            sources=get_sources(data),
            upvotes=get_upvotes(data),
            downvotes=get_downvotes(data),
            rating=get_rating(data),
        )
        await posts.insert(post, validate=False)


    async def update_post(post:schemas.Post, data: V):
        original_post = post.copy()
        post.tags=get_tags(data)
        post.sources=get_sources(data)
        post.upvotes=get_upvotes(data)
        post.downvotes=get_downvotes(data)
        post.rating=get_rating(data)
        
        if post != original_post:
            database.Post.update(post.id, original_post)


    async def process_post(data: V):
        try:
            hashes = get_hashes(data)
            post = database.Post.md5_get(hashes.md5s[0])
        except KeyError:
            await import_post(data)
        else:
            await update_post(post, data)


    counter = [] # Terrible hack for variable scope, need a mutable counter
    async def handle_post(data: V):
        try:
            await process_post(data)
        except Exception as e:
            logging.exception(e)
        else:
            counter.append(None)

        if limit and len(counter) >= limit:
            raise Exception

    if inspect.isasyncgen(iterable):
        async for post in iterable:
            try:
                await handle_post(post)
            except Exception:
                return
    else:
        for post in iterable:
            try:
                await handle_post(post)
            except Exception:
                return