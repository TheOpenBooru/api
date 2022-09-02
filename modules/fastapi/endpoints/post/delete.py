from . import router
from modules import database, fastapi
from fastapi import Response, Depends


@router.delete("/{id}",
    status_code=200,
    responses={},
    dependencies=[Depends(fastapi.RequirePermission("canDeletePosts"))],
)
async def delete_post(id:int):
    database.Post.delete(id)
    return Response(status_code=200)
