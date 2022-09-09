from itertools import count
from typing import Union
import bs4
import requests


async def safebooru_search(search:str,limit:Union[int,None]) -> list[dict]:
    url = f"https://safebooru.org/index.php?page=dapi&s=post&q=index&tags={search}"
    found_posts = []
    for x in count():
        r = requests.get(
            url=url,
            params={
                "limit":1000,
                "pid":x,
            }
        )
        xml = bs4.BeautifulSoup(r.text,"xml")
        new_posts = xml.find_all('post')
        found_posts.extend(new_posts)
        
        if len(new_posts) != 1000:
            break
        if limit and len(found_posts) >= limit:
            break
    posts = [x.attrs for x in found_posts]
    return posts