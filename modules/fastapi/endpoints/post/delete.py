from . import router
from modules import database, fastapi
from modules.fastapi import RequirePermission
from fastapi import Response, Depends


@router.delete("/{id}",
    operation_id="delete_post",
    responses={},
    dependencies=[
        Depends(RequirePermission("canDeletePosts"))
    ],
)
async def delete_post(id:int):
    database.Post.delete(id)
    return Response(status_code=200)
