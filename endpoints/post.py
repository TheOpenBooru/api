from .dependencies.auth import parse_token
from modules import schemas
from modules.auth.jwt import TokenData
from modules.search import searchPosts,parseBSLs
from modules.database import Post
from fastapi import APIRouter,Response,status,Depends

router = APIRouter()

@router.get("/post",response_model=schemas.Post, tags=["Unprivileged"])
async def get_post(id:int):
    post = Post.get(id=id)
    if post:
        return post.to_pydantic()
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.patch('/post', tags=['User'])
async def edit_post(id:int,post:schemas.Post,token:TokenData=Depends(parse_token)):
    if token.level == "ADMIN":
        Post.update(id=id,**post.dict())
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,content="Not High Enough Level")


@router.delete("/post", tags=['Admin'])
async def delete_post(id:int ,token:TokenData=Depends(parse_token)):
    if token.level == "ADMIN":
        Post.delete(id)
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,content="Not High Enough Level")


@router.post("/create", tags=['User'])
async def create_post():
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/search", response_model=list[schemas.Post], tags=["Unprivileged"])
async def search_posts(query:str):
    search_settings = parseBSLs(query)
    posts = searchPosts(search_settings)
    return posts
