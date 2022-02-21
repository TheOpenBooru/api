from . import router
from modules import database
from fastapi import Response,status

@router.delete("/post/{id}")
async def delete_post(id:int):
    if database.Post.get(id=id) is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        database.Post.delete(id)
        return Response(status_code=status.HTTP_202_ACCEPTED)
