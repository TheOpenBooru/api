from . import router
from endpoints._token import DecodeToken,Account
from modules import database
from fastapi import Response, Depends


@router.delete("/post/{id}",
    responses={
        204:{"description":"Post Successfully Deleted"},
        401:{"description":"You Were Not Authorised To Delete This Post"},
    },
)
async def delete_post(id:int,user:Account=Depends(DecodeToken)):
    if user.permissions.canDeletePosts:
        database.Post.delete(id)
        return Response(status_code=204)
    else:
        return Response(status_code=401)
