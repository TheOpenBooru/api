from .dependencies.auth import parse_token
from modules import schemas
from modules.search import searchPosts,parseBSLs
from modules.database import Post,User
from fastapi import APIRouter,Response,status,UploadFile,Depends

router = APIRouter()

@router.get("/post/{id}",response_model=schemas.Post, tags=["Unprivileged"])
async def get_post(id:int):
    try:
        post = Post.get(id=id)
    except KeyError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return post


@router.patch('/post/{id}')
async def edit_post(id:int,tokenData = Depends(parse_token)):
    if tokenData:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete("/post/{id}")
async def delete_post(id:int):
    Post.delete(id)


@router.post("/create")
async def create_post():
    """
    Create a new post
    """
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/search", response_model=list[schemas.Post], tags=["Unprivileged"])
async def search_posts(query:str):
    posts = searchPosts(parseBSLs(query))
    return posts
