import time
import hashlib
from modules import store,types
from modules.search import searchPosts,parseBSLs
from modules.database import Post,User,types
from fastapi import APIRouter, Response,status,UploadFile
from pydantic import BaseModel

router = APIRouter()

@router.get("/get/{id}", response_model=types.Post)
def get_post(id:int):
    try:
        post = Post.get(id=id)
    except KeyError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(post)

userID = User.create('example','test@example.com')
@router.post("/create")
async def create_post(file: UploadFile):
    ID = str(time.time())
    imgData:bytes = file.file.read()
    store.put(ID,imgData)
    types.Image()
    
    md5 = hashlib.md5(imgData).hexdigest()
    sha256 = hashlib.sha256(imgData).hexdigest()
    Post.create(
        userID,imgID,imgID,imgID,
        md5,sha256,
        'image',False)
    return Response(status_code=status.HTTP_201_CREATED)

@router.get("/search", response_model=list[types.Post])
def search_posts(query:str):
    posts = searchPosts(parseBSLs(query))
    return Response(posts)
