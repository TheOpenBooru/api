import requests
import mimetypes
import bs4
from dataclasses import dataclass
from modules import database

@dataclass
class Post:
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

def generate():
    r = requests.get("https://safebooru.org/index.php?page=dapi&s=post&q=index",
                params={
                    "limit":4000,
                    "tags":["rating:safe"]
                    })
    xml = bs4.BeautifulSoup(r.text,'lxml')
    posts = list(xml.find('posts').children)
    print(f"Using {len(posts)} Posts")
    for x in posts:
        try:
            post = Post(**x.attrs)
        except:
            continue
        full = database.types.Image(
            post.file_url,
            post.height,post.width,
            mimetypes.guess_type(post.file_url)[0]
            )
        preview = database.types.Image(
            post.preview_url,
            post.preview_height,post.preview_width,
            mimetypes.guess_type(post.preview_url)[0]
            )
        sample = database.types.Image(
            post.sample_url,
            post.sample_height,post.sample_width,
            mimetypes.guess_type(post.sample_url)[0]
            )
        type = mimetypes.guess_type(post.sample_url)[0].split('/')[0]
        postID = database.Post.create(
            post.creator_id,
            full,preview,sample,
            post.md5,post.md5*2,
            type,False
            )
        database.Post.set(
            postID,
            source=post.source,
            rating='safe',
            tags=' '.split(post.tags),
            )