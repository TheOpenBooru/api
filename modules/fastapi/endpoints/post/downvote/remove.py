from . import router
from modules import database, posts
from modules.fastapi.dependencies import DecodeToken, RequirePermission
from fastapi import Response, Depends

@router.post("/{id}/downvote/remove",
    operation_id="remove_downvote",
    dependencies=[
        Depends(RequirePermission("canVotePosts")),
    ],
)
async def remove_downvote(id:int, account: DecodeToken = Depends()):
    if not database.Post.exists(id):
        return Response("Post Not Found", status_code=404)
    else:
        posts.remove_downvote(id, account.id)
        return Response("Success")
