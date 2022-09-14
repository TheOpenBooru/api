from . import router
from modules import schemas, posts
from modules.fastapi.dependencies import RequirePermission
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional


@router.get("/search",
    operation_id="search_posts",
    response_model=list[schemas.Post],
    dependencies=[
        Depends(RequirePermission("canSearchPosts")),
    ]
)
async def search_posts(
        query: schemas.PostQuery = Depends(),
        media_types: list[schemas.MediaType] = Query(default=[], description="Media Types to include"),
        ratings: list[schemas.Rating] = Query(default=[], description="Ratings to exclude from the results"),
        include_tags: list[str] = Query(default=[]),
        exclude_tags: list[str] = Query(default=[]),
        ids:list[int] = Query(default=[]),
        ):
    query.media_types = media_types
    query.ratings = ratings
    query.include_tags = include_tags
    query.exclude_tags = exclude_tags
    query.ids = ids
    searched_posts = await posts.search(query)
    return JSONResponse(
        content=jsonable_encoder(searched_posts),
        headers={"Cache-Control": "max-age=15, public"},
    )
