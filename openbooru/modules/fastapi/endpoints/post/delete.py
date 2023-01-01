from . import router
from openbooru.modules import database, fastapi
from openbooru.modules.fastapi import PermissionManager
from fastapi import Response, Depends


@router.delete("/{id}",
    responses={},
    dependencies=[
        Depends(PermissionManager("canDeletePosts"))
    ],
)
async def delete_post(id:int):
    database.Post.delete(id)
    return Response(status_code=200)
