from . import router
from openbooru.modules import database, posts
from openbooru.modules.fastapi.dependencies import PermissionManager
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/ids",
    response_model=list[int],
    dependencies=[
        Depends(PermissionManager("canSearchPosts")),
    ]
)
async def get_post_ids():
    ids = database.Post.ids()
    return JSONResponse(
        content=jsonable_encoder(ids),
        headers={"Cache-Control": "max-age=3600, public"},
    )
