from . import router
from modules.database import Post
from fastapi import Response,status

@router.delete("/post/{id}")
async def delete_post(id:int):
    if not Post.exists(id):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
