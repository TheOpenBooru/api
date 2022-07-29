from . import router
from modules import database, posts
from modules.fastapi.dependencies import DecodeToken, RequirePermission, Account
from fastapi import Response, Depends


@router.post("/{id}/downvote/add",
    responses={
        202:{"description":"Success"},
        404:{"description":"Post Not Found"},
    },
    dependencies=[Depends(RequirePermission("canVotePosts"))],
)
async def add_downvote(id:int, account: Account = Depends(DecodeToken)):
    if not database.Post.exists(id):
        return Response("Post Not Found", status_code=404)
    else:
        posts.add_downvote(id, account.id)
        return Response("Success", status_code=200)
