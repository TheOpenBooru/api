from typing import Union, Generator
from itertools import count
import requests

USER_AGENT = "Openbooru/1.0 (by NoHomoZone)"

def guess_post_count(hostname: str) -> int:
    POST_DELETION_RATIO = 1.16

    r = requests.get(
        f"https://{hostname}/posts.json",
        params={"limit":1},
        headers={ "User-Agent": USER_AGENT}
    )
    json = r.json()
    posts = json["posts"]
    first_id = posts[0]["id"]
    return first_id / POST_DELETION_RATIO


def iter_over_posts(hostname: str) -> Generator[dict, None, None]:
    for x in count():
        posts = download_page(hostname, x)
        if len(posts) == 0:
            return
        
        for post in posts:
            yield post


def download_page(hostname: str, page: int) -> list[dict]:
    LIMIT = 320
    start_id = LIMIT * page
    end_id = LIMIT * (page + 1)
    
    r = requests.get(
        f"https://{hostname}/posts.json",
        params={
            "tags":["order:id", f"id:{start_id}..{end_id}"],
            "limit":LIMIT,
        },
        headers={ "User-Agent": USER_AGENT}
    )
    json = r.json()
    posts = json["posts"]
    return posts
