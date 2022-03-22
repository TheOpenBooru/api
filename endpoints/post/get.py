from . import router
from modules import schemas,database
from fastapi import Response,status,responses


@router.get("/post/{id}",response_model=schemas.Post)
async def get_post(id:int):
    CACHE_HEADER = {"Cache-Control": "max-age=60, public"}
    post = database.Post.get(id=id)
    if post:
        database.Post.increment_view(id)
        return responses.Response(
            content=post.json(),
            headers=CACHE_HEADER
        )
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
