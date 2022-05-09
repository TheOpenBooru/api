from . import router
from modules import schemas
from modules.database import Post
from fastapi import Response,status,responses


@router.get("/post/{id}",response_model=schemas.Post)
async def get_post(id:int):
    CACHE_HEADER = {"Cache-Control": "max-age=60, private"}
    if Post.exists(id):
        Post.increment_view(id)
        post = Post.get(id)
        return responses.Response(
            content=post.json(),
            headers=CACHE_HEADER
        )
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
