from . import router
from modules import database, posts
from modules.fastapi.dependencies import DecodeToken, RequirePermission, Account
from fastapi import Response, Depends


@router.post("/{id}/downvote/add")
async def add_downvote(id:int, account: Account = Depends(DecodeToken)):
    if not database.Post.exists(id):
        return Response("Post Not Found", status_code=404)
    else:
        posts.add_downvote(id, account.id)
        return Response("Success")
