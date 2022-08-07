from . import utils, URLImporter, ImportFailure
from modules import settings, schemas, database, posts
from urllib.parse import parse_qs, urlparse
import logging
from tqdm import tqdm
from datetime import datetime
import bs4
import requests
import ujson


class Rule34(URLImporter):
    enabled = settings.RULE34_ENABLED
    def __init__(self):
        try:
            requests.get("https://rule34.xxx/",timeout=2)
        except Exception:
            self.functional = False
        else:
            self.functional = True


    def is_valid_url(self,url:str) -> bool:
        return url.startswith("https://rule34.xxx/index.php?page=post&s=view&id=")


    async def download_url(self,url:str) -> list[schemas.Post]:
        try:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query)
            id = query['id'][0]
        except Exception:
            raise ImportFailure("Could not extract ID from the URL")
        
        post_data = post_from_id(id)
        tags = extract_tags(post_data)
        source = extract_source(post_data)
        url = post_data['file_url']
        
        data,filename = utils.download_url(url)
        post = await posts.generate(data,filename,
            additional_tags=tags,
            source=source,
        )
        return [post]


    async def load_default(self):
        if settings.RULE34_IMPORT == False:
            return
        if settings.RULE34_DUMP_LOCATION == None:
            logging.warning("Rule34 dump location not set, cannot import")
            return
        
        dump_location:str = settings.RULE34_DUMP_LOCATION # type: ignore
        limit = settings.RULE34_LIMIT
        

        with open(dump_location) as f:
            posts = ujson.load(f)
        
        if limit:
            posts = posts[:limit]
        
        for post in tqdm(posts, desc="Importing Rule34"):
            try:
                post = await post_from_dict(post)
                database.Post.insert(post)
            except Exception as e:
                continue


def post_from_id(id:str) -> dict:
    url = "https://rule34.xxx/index.php?page=dapi&s=post&q=index"
    r = requests.get(url,params={'id':id})
    soup = bs4.BeautifulSoup(r.text,'html.parser')
    tag: bs4.Tag = soup.find('post') # type: ignore
    
    if tag == None:
        raise ImportFailure("Rule34 Post Does Not Exist")
    else:
        return tag.attrs


def extract_tags(post_data:dict) -> list[str]:
    tag_string = post_data['tags']
    tags = tag_string.split(' ')
    tags = utils.normalise_tags(tags)
    return tags


def extract_source(post_data:dict) -> str:
    id = post_data['id']
    source = post_data['source']
    if source:
        return source
    else:
        return f"https://rule34.xxx/index.php?page=post&s=view&id={id}"