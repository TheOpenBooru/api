from itertools import count
from modules import settings
from typing import Union, Generator
from e621.models import Post
from e621.api import E621


api = E621()
class OutOfPostsException(Exception): pass


def iter_over_posts() -> Generator[dict, None, None]:
    limit = 0
    for x in count():
        try:
            posts = download_page(x)
        except OutOfPostsException:
            return
        else:
            for post in posts:
                yield post



def download_page(page:int) -> list[dict]:
    LIMIT = 320
    start_id = LIMIT * page
    end_id = LIMIT * (page + 1)
    posts = api.posts.search(
        tags=["order:id", f"id:{start_id}..{end_id}"],
        limit=LIMIT,
    )

    raw_posts = [_parse_post(x) for x in posts]
    return raw_posts


def _parse_post(post:Post) -> dict:
    del post.e621api
    data = post.dict()
    return data

