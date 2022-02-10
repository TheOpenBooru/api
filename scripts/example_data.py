import bs4
import json
import requests
import mimetypes
from pathlib import Path
from dataclasses import dataclass
from modules import validate
from modules.database import User,Post,Tag,types

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
                    "tags":["rating:safe sort:score"]
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

def generate():
    createdUsers = set()
    if not cache_path.exists():
        _load_data_to_json()
    
    with open(cache_path) as f:
        posts = json.load(f)
        
    for x in posts:
        post = SafeBooruPost(**x)
        creatorID = post.creator_id
        if creatorID not in createdUsers:
            createdUsers.add(creatorID)
            user:types.User = User.create(str(creatorID),f"{creatorID}@example.com")
        else:
            user:types.User = User.get(name=str(creatorID))
        full = types.Image(post.file_url,post.height,post.width,'image/jpeg')
        preview = types.Image(post.sample_url,post.sample_height,post.sample_width,'image/jpeg')
        thumbnail = types.Image(post.preview_url,post.preview_height,post.preview_width,mimetype='image/jpeg')
        type = mimetypes.guess_type(post.sample_url)[0].split('/')[0]
        if Post.get(md5=post.md5):
            return
        newPost = Post.create(
            creator=user.id,md5=post.md5,
            type=type,sound=False,
            full=full
            )
        newPost.thumbnail = thumbnail
        newPost.preview = preview
        for tag in newPost.tags:
            if not Tag.get(name=tag):
                try:
                    validate.tag(tag)
                except ValueError:
                    continue
                else:
                    Tag.create(name=tag,namespace='generic')
        newPost.tags = post.tags.split(' ')
        Post.update(newPost.id,newPost)