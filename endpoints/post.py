from ..modules.database import post
from fastapi import Response, Query,APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/get')
def posts_get(post_ids: list[int]  = Query(None,max_length=30)):
    if not post_ids:
        return Response(status_code=400)
    posts = post.search(post_ids=post_ids)
    return posts

def post_search(tags:list[str] = Query(None),sort:str = None,limit:int = None):
    posts = post.search(tags=['test'])
    
    return posts

