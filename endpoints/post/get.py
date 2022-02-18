from . import router
from modules import schemas,database
from fastapi import Response,status


@router.get("/post/{id}",response_model=schemas.Post, tags=["Unprivileged"])
async def get_post(id:int):
    post = database.Post.get(id=id)
    if post:
        return post.to_pydantic()
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
