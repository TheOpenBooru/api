import bs4
import json
import time
import requests
import mimetypes
from pathlib import Path
from dataclasses import dataclass
from modules.database import User,Post
from modules import schemas

@dataclass
class SafeBooruPost:
    id: int
    creator_id: int
    md5: str
    rating: str
    
    file_url: str
    height: int
    width:int
    
    preview_url: str
    preview_height: int
    preview_width: int
    
    sample_url: str
    sample_height: int
    sample_width: int
    
    source: str
    tags: str
    change:str
    created_at:str
    has_children:str
    has_comments:str
    has_notes:str
    parent_id:str
    score:str
    status:str


cache_path = Path("./data/example_data.json")
def _load_data_to_json():
    r = requests.get("https://safebooru.org/index.php?page=dapi&s=post&q=index",
                params={
                    "limit":100,
                    "tags":["rating:safe -video -gif"],
                    })
    xml = bs4.BeautifulSoup(r.text,'lxml')
    xmlPosts = list(xml.find('posts').children)
    posts = []
    for x in xmlPosts:
        try:
            posts.append(dict(**x.attrs))
        except:
            continue
    
    with open(cache_path, "w") as f:
        json.dump(posts,f)


def construct_post(post:SafeBooruPost) -> schemas.Post:
    full =  schemas.Image(
        url=post.file_url,
        height=post.height,width=post.width,
        mimetype='image/jpeg'
    )
    preview = schemas.Image(
        url=post.sample_url,
        height=post.sample_height,width=post.sample_width,
        mimetype='image/jpeg'
    )
    thumbnail = schemas.Image(
        url=post.preview_url,
        height=post.preview_height,
        width=post.preview_width,
        mimetype='image/jpeg'
    )
    type = mimetypes.guess_type(post.sample_url)[0].split('/')[0]
    tags = post.tags.split(' ')
    tags = tags[1:-1] # remove first and last empty tags
    return schemas.Post(
        id=Post.get_unused_id(),uploader=0,
        full=full,preview=preview,thumbnail=thumbnail,
        md5s=[post.md5],tags=tags,type=type,
        language='eng',age_rating='safe',
    )

def generate():
    if not cache_path.exists():
        _load_data_to_json()
    
    with open(cache_path) as f:
        posts = json.load(f)
    
    for x in posts:
        raw_post = SafeBooruPost(**x)
        if Post.get(md5=raw_post.md5):
            continue
        post = construct_post(raw_post)
        Post.create(post)