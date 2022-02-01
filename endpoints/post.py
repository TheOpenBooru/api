from . import types
from modules import auth,search,image
from modules.database import Post
from fastapi import APIRouter, Header,Response,status
from pydantic import BaseModel

router = APIRouter()

class CreatePost(BaseModel):
    image: bytes
    source: str
    rating: str

@router.get("/get/{id}", response_model=types.Post)
def get_post(id:int):
    return Post.get(id=id)

@router.post("/create",response_model=dict,status_code=status.HTTP_201_CREATED)
def create_post(data:CreatePost,Authorization:str=Header(None)):
    if not Authorization:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    data.image
    userID = auth.jwt.decode(Authorization)['user_id']
    Post.create(userID)

@router.get("/search", response_model=list[types.Post])
def search_posts(query:str,Authorization:str=Header(None)):
    config = search.BSLs.parseBSLs(query)
