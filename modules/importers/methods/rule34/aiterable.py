import grequests

from modules import settings
import requests
from typing import Union
import bs4
from itertools import count


class OutOfPostsException(Exception): pass
PAGE_LIMIT = 1000

def roundDivide(a:Union[int, float],b:Union[int, float]):
    return int(a / b) + 1


def iter_over_posts(limit: Union[int, None]):
    max_id = _get_top_id()
    page_count = roundDivide(max_id, PAGE_LIMIT)
    if limit:
        page_limit = roundDivide(limit, PAGE_LIMIT)
        page_count = min(page_count, page_limit)

    REQ_COUNT = 15
    for x in range(roundDivide(page_count, REQ_COUNT)):
        start = REQ_COUNT * x
        end = REQ_COUNT + start
        reqs = [download_page(x) for x in range(start, end)]

        for r in grequests.imap(reqs, size=REQ_COUNT):
            try:
                posts = parse_page(r.text)
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


def download_page(index:int) -> grequests.AsyncRequest:
    start = PAGE_LIMIT * index
    end = PAGE_LIMIT * (index + 1)
    
    return grequests.get(
        "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index",
        params={
            "tags":f"id:>{start} id:<{end}",
            "limit":PAGE_LIMIT,
        },
    )


def parse_page(page:str) -> list[dict]:
    soup = bs4.BeautifulSoup(page,'xml')
    posts = [x.attrs for x in soup.find_all("post")]
    
    if len(posts) == 0:
        raise OutOfPostsException
    else:
        return posts
