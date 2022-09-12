from . import router
from modules import database, posts
from modules.fastapi.dependencies import DecodeToken, RequirePermission
from fastapi import Response, Depends


@router.post("/{id}/upvote/add",
    operation_id="add_upvote",
    dependencies=[
        Depends(RequirePermission("canVotePosts")),
    ],
)
async def add_upvote(id:int, account: DecodeToken = Depends()):
    if not database.Post.exists(id):
        return Response("Post Not Found", status_code=404)
    else:
        posts.add_upvote(id, account.id)
        return Response("Success")
