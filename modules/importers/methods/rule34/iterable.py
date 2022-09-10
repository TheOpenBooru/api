from __future__ import annotations
from typing import Union
import bs4
import requests
from requests_futures.sessions import FuturesSession

class OutOfPostsException(Exception): pass
PAGE_LIMIT = 1000

def PagesRequired(posts:int):
    return int(posts / 1000) + 1


def iter_over_posts(limit: Union[int, None]):
    count = 0
    max_id = _get_top_id()
    page_count = PagesRequired(max_id)

    REQ_COUNT = 25
    session = FuturesSession(max_workers=REQ_COUNT)
    
    for x in range(int(page_count / REQ_COUNT) + 1):
        start = REQ_COUNT * x
        end = REQ_COUNT + start
        reqs = [download_page(session,x) for x in range(start, end)]

        for req in reqs:
            r = req.result()
            
            try:
                posts = parse_page(r.text)
            except OutOfPostsException:
                return
            else:
                for post in posts:
                    count += 1
                    if limit and count > limit:
                        return
                    else:
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


def download_page(session: FuturesSession, index:int):
    start = PAGE_LIMIT * index
    end = PAGE_LIMIT * (index + 1)
    
    return session.get(
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
 