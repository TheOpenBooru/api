from . import router
from modules.database import Post
from fastapi import Response,status

responses = {
    401:{"description":"You Were Not Authorised To Delete This Post"},
    404:{"description":"The Post Could Not Be Found"},
}

@router.delete("/post/{id}",
    responses=responses, # type: ignore
)
async def delete_post(id:int):
    if not Post.exists(id):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
