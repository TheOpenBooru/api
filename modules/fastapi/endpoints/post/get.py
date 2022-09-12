from . import router
from modules import schemas
from modules.fastapi.dependencies import RateLimit, RequirePermission
from modules.database import Post
from fastapi import Response, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/{id}",
    operation_id="get_post",
    response_model=schemas.Post,
    dependencies=[
        Depends(RequirePermission("canViewPosts")),
    ]
)
async def get_post(id:int):
    CACHE_HEADER = {"Cache-Control": "max-age=60, public"}
    if not Post.exists(id):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        post = Post.get(id)
        return JSONResponse(
            content=jsonable_encoder(post),
            headers=CACHE_HEADER,
        )
