from . import router
from modules import schemas, posts
from modules.fastapi.dependencies import RateLimit, RequirePermission
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional


@router.get("/search",
    response_model=list[schemas.Post],
    dependencies=[
        Depends(RequirePermission("canSearchPosts")),
        Depends(RateLimit("40/minute")),
        Depends(RateLimit("3/second")),
    ]
)
async def search_posts(
        query: schemas.Post_Query = Depends(),
        media_types: list[schemas.Media_Type] = Query(default=[], description="Media Types to include"),
        ratings: list[schemas.Ratings] = Query(default=[], description="Ratings to exclude from the results"),
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
