import inspect
from openbooru.modules import database, posts, schemas
from openbooru.modules.importers import DownloadFailure
from openbooru.modules.schemas import Media, Image, Hashes, Rating, Post
from typing import Callable, TypeVar, AsyncIterable, Iterable
import time
import logging


class ReachedPostLimit(Exception): pass
Data = TypeVar("Data")


async def run_importer(
    iterable: AsyncIterable[Data] | Iterable[Data],
    limit: int | None,
    get_hashes: Callable[[Data], Hashes],
    get_images: Callable[[Data], tuple[Media, Media | None, Image]],
    update_existing: bool = True,
    get_tags: Callable[[Data], list[str]] | None = None,
    get_created_at: Callable[[Data], float] | None = None,
    get_upvotes: Callable[[Data], int] | None = None,
    get_downvotes: Callable[[Data], int] | None = None,
    get_sources: Callable[[Data], list[str]] | None = None,
    get_rating: Callable[[Data], Rating] | None = None,
):
    get_tags = get_tags or default_get_tags
    get_created_at = get_created_at or default_get_created_at
    get_upvotes = get_upvotes or default_get_upvotes
    get_downvotes = get_downvotes or default_get_downvotes
    get_sources = get_sources or default_get_sources
    get_rating = get_rating or default_get_rating


    async def import_post(data: Data):
        full, preview, thumbnail = get_images(data)
        post = Post(
            id=database.Post.generate_id(),
            full=full,
            preview=preview,
            thumbnail=thumbnail,
            hashes=get_hashes(data),
            created_at=get_created_at(data),
            tags=get_tags(data),
            sources=get_sources(data),
            upvotes=get_upvotes(data),
            downvotes=get_downvotes(data),
            rating=get_rating(data),
        )
        await posts.insert(post, validate=False)


    async def update_post(post: Post, data: Data):
        original_post = post.copy()
        post.tags = get_tags(data)
        post.sources = get_sources(data)
        post.upvotes = get_upvotes(data)
        post.downvotes = get_downvotes(data)
        post.rating = get_rating(data)

        if post != original_post:
            database.Post.update(post.id, post)

    async def process_post(data: Data):
        try:
            hashes = get_hashes(data)
            post = database.Post.md5_get(hashes.md5s[0])
        except KeyError:
            await import_post(data)
        else:
            if update_existing:
                await update_post(post, data)


    counter = 0
    async def handle_post(data: Data):
        nonlocal counter
        try:
            await process_post(data)
        except DownloadFailure:
            pass  # Explicit Exception, downloader could not import post
        except Exception as e:
            logging.exception(e)
        else:
            counter += 1

        if limit and counter >= limit:
            raise ReachedPostLimit


    try:
        if inspect.isasyncgen(iterable):
            async for post in iterable:
                await handle_post(post)
        else:
            for post in iterable: # type: ignore
                await handle_post(post)
    except ReachedPostLimit: # Imported required number of posts
        return


def default_get_tags(*args):
    return []


def default_get_created_at(*args):
    return time.time()


def default_get_upvotes(*args):
    return 0


def default_get_downvotes(*args):
    return 0


def default_get_sources(*args):
    return []


def default_get_rating(*args):
    return Rating.unrated
