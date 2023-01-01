from . import router
from openbooru.modules import schemas
from openbooru.modules.fastapi.dependencies import RateLimit, PermissionManager
from openbooru.modules.database import Post
from fastapi import Response, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/{id}",
    response_model=schemas.Post,
    dependencies=[
        Depends(PermissionManager("canViewPosts")),
    ]
)
async def get_post(id:int):
    CACHE_HEADER = {"Cache-Control": "max-age=300, public"}
    try:
        post = Post.get(id)
    except KeyError:
        raise HTTPException(404, "Post Does Not Exist")
    else:
        return JSONResponse(
            content=jsonable_encoder(post),
            headers=CACHE_HEADER,
        )
