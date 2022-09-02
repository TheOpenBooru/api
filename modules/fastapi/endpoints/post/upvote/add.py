from . import router
from modules import database, posts
from modules.fastapi.dependencies import DecodeToken, Account
from fastapi import Response, Depends


@router.post("/{id}/upvote/add")
async def add_upvote(id:int, account: Account = Depends(DecodeToken)):
    if not database.Post.exists(id):
        return Response("Post Not Found", status_code=404)
    else:
        posts.add_upvote(id, account.id)
        return Response("Success")
