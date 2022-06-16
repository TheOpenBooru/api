from . import router
from modules import schemas
from modules.database import Post
from fastapi import Response,status


@router.get("/post/{id}",
    response_model=schemas.Post,
    status_code=status.HTTP_200_OK,
    responses={
        200:{"description":"Successfully Retrieved Post"},
        404:{"description":"The Post Could Not Be Found"},
    },
)
async def get_post(id:int):
    CACHE_HEADER = {"Cache-Control": "max-age=60, private"}
    if Post.exists(id):
        post = Post.get(id)
        return Response(
            content=post.json(),
            headers=CACHE_HEADER,
            status_code=status.HTTP_200_OK,
        )
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
