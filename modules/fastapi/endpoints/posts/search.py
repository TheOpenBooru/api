from . import router
from modules import schemas, posts
from modules.fastapi.dependencies import PermissionManager
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional

class PostQueryParams(schemas.PostQuery):
    media_types: list[schemas.MediaType] = Query(default=[], description="Media Types to include")
    ratings: list[schemas.Rating] = Query(default=[], description="Ratings to exclude from the results")
    include_tags: list[str] = Query(default=[])
    exclude_tags: list[str] = Query(default=[])
    ids:list[int] = Query(default=[])


@router.get("/search",
    operation_id="search_posts",
    response_model=list[schemas.Post],
    dependencies=[
        Depends(PermissionManager("canSearchPosts")),
    ]
)
async def search_posts(query: PostQueryParams = Depends()):
    searched_posts = await posts.search(query)
    return JSONResponse(
        content=jsonable_encoder(searched_posts),
        headers={"Cache-Control": "max-age=15, public"},
    )
