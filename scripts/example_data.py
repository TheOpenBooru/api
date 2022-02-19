import bs4
import json
import time
import requests
import mimetypes
from pathlib import Path
from dataclasses import dataclass
from modules.database import User,Post,types

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
                    "limit":2000,
                    "tags":["rating:safe"]
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


createdUsers = {}
def _get_user_id(post:SafeBooruPost):
    creatorID = post.creator_id
    if creatorID not in createdUsers:
        user:types.User = User.create(str(creatorID),f"{creatorID}@example.com")
        createdUsers[creatorID] = user.id
    return createdUsers[creatorID]

def construct_post(post:SafeBooruPost) -> types.Post:
    full = types.Image(post.file_url,post.height,post.width,'image/jpeg')
    preview = types.Image(post.sample_url,post.sample_height,post.sample_width,'image/jpeg')
    thumbnail = types.Image(post.preview_url,post.preview_height,post.preview_width,mimetype='image/jpeg')
    type = mimetypes.guess_type(post.sample_url)[0].split('/')[0]
    usedID = _get_user_id(post)
    return types.Post(
        id=None,creator=usedID,
        created_at=int(time.time()),
        full=full,preview=preview,thumbnail=thumbnail,
        md5s=[post.md5],sha256s=[],
        type=type,sound=False
    )

def generate():
    if not cache_path.exists():
        _load_data_to_json()
    
    with open(cache_path) as f:
        posts = json.load(f)
    
    for x in posts:
        raw_post = SafeBooruPost(**x)
        if Post.get(md5=raw_post.md5):
            return
        post = construct_post(raw_post)
        Post.create(post)