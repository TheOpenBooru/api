from __future__ import annotations
import bs4
import requests
import logging
from requests_futures.sessions import FuturesSession
from concurrent.futures._base import Future


class OutOfPostsException(Exception): pass
PAGE_LIMIT = 1000

def PagesRequired(posts:int):
    return int(posts / 1000) + 1


def iter_over_posts(hostname:str):
    max_id = get_top_id(hostname)
    page_count = PagesRequired(max_id)

    REQ_COUNT = 25
    session = FuturesSession(max_workers=REQ_COUNT)
    
    for x in range(int(page_count / REQ_COUNT) + 1):
        start = REQ_COUNT * x
        end = REQ_COUNT + start
        reqs = [download_page(x, hostname, session) for x in range(start, end)]

        for req in reqs:
            try:
                req:Future
                r = req.result()
            except Exception:
                logging.warning(f"{hostname}, Failed to Retrieved Posts")
                continue
            
            posts = parse_page(r.text)

            if len(posts) == 0:
                return
            
            for post in posts:
                yield post


def get_top_id(hostname: str) -> int:
    url = f"https://{hostname}/index.php?page=dapi&s=post&q=index&limit=1"
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'xml')
    post = soup.find("post")
    top_id = post.attrs.get("id", "5000000")  # type: ignore
    return int(top_id)


def guess_post_count(hostname: str) -> int:
    POST_DELETION_RATIO = 0.882
    top_id = get_top_id(hostname)
    count_estimate = int(top_id * POST_DELETION_RATIO)
    return count_estimate


def download_page(index: int, hostname:str, session: requests.Session|None = None):
    start = PAGE_LIMIT * index
    end = PAGE_LIMIT * (index + 1)
    if session == None:
        session = requests.Session()
    
    return session.get(
        f"https://{hostname}/index.php?page=dapi&s=post&q=index",
        params={
            "tags":f"id:>{start} id:<{end}",
            "limit":PAGE_LIMIT,
        },
    )


def parse_page(page: str) -> list[dict]:
    soup = bs4.BeautifulSoup(page,'xml')
    posts = [x.attrs for x in soup.find_all("post")]
    posts = [post for post in posts if post["width"] != ""]
    return posts
 