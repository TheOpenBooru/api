from modules import settings
import requests
from typing import Union
import bs4
from itertools import count


class OutOfPostsException(Exception): pass
PAGE_LIMIT = 1000


def iter_over_posts(limit: Union[int, None]):
    max_id = _get_top_id()
    page_count = int(max_id // PAGE_LIMIT) + 1
    if limit:
        page_limit = int(limit // PAGE_LIMIT) + 1
        page_count = min(page_count, page_limit)
    
    for x in range(page_count):
        try:
            page = download_page(x)
            posts = parse_page(page)
        except OutOfPostsException:
            return
        else:
            for post in posts:
                yield post


def _get_top_id() -> int:
    r = requests.get("https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1")
    soup = bs4.BeautifulSoup(r.text, 'xml')
    post = soup.find("post")
    top_id = post.attrs.get("id", "6400000")
    return int(top_id)


def guess_post_count() -> int:
    POST_DELETION_RATIO = 0.882
    top_id = _get_top_id()
    count_estimate = int(top_id * POST_DELETION_RATIO)
    return count_estimate


def download_page(index:int) -> str:
    start = PAGE_LIMIT * index
    end = PAGE_LIMIT * (index + 1)
    
    r = requests.get(
        "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index",
        params={
            "tags":f"id:>{start} id:<{end}",
            "limit":PAGE_LIMIT,
        },
    )
    return r.text


def parse_page(page:str) -> list[dict]:
    soup = bs4.BeautifulSoup(page,'xml')
    posts = [x.attrs for x in soup.find_all("post")]
    
    if len(posts) == 0:
        raise OutOfPostsException
    else:
        return posts
