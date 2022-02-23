from . import router
from modules import schemas,database
from fastapi import Response,status


@router.get("/post/{id}",response_model=schemas.Post)
async def get_post(id:int):
    post = database.Post.get(id=id)
    if post:
        database.Post.increment_view(id)
        return post
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
