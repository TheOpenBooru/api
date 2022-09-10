from . import router
from modules import database, posts
from modules.fastapi.dependencies import DecodeToken, RequirePermission
from fastapi import Response, Depends


@router.post("/{id}/downvote/add",
    dependencies=[
        Depends(RequirePermission("canVotePosts")),
    ],
)
async def add_downvote(id:int, account: DecodeToken = Depends()):
    if not database.Post.exists(id):
        return Response("Post Not Found", status_code=404)
    else:
        posts.add_downvote(id, account.id)
        return Response("Success")
