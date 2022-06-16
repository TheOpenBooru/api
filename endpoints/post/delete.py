from . import router
from modules import database, account
from modules.dependencies import DecodeToken, RequirePermission
from fastapi import Response, Depends


@router.delete("/post/{id}",
    responses={
        204:{"description":"Post Successfully Deleted"},
        401:{"description":"You Were Not Authorised To Delete This Post"},
    },
    dependencies=[Depends(RequirePermission("canDeletePosts"))],
)
async def delete_post(id:int):
    database.Post.delete(id)
    return Response(status_code=204)
