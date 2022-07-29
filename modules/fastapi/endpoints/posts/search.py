from . import router
from modules import schemas, posts
from modules.fastapi.dependencies import RateLimit
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional


@router.get("/search",
    response_model=list[schemas.Post],
    status_code=200,
    responses={
        200:{"description":"Successfully Retrieved"},
    },
    dependencies=[
        Depends(RateLimit("2/second")),
    ]
)
async def search_posts(
    query: schemas.Post_Query = Depends(),
    exclude_ratings: list[schemas.Valid_Post_Ratings] = Query(default=[], description="Ratings to exclude from the results"),
    include_tags: list[str] = Query(default=[]),
    exclude_tags: list[str] = Query(default=[]),
    ids:list[int] = Query(default=[]),
    ):
    query.exclude_ratings = exclude_ratings
    query.include_tags = include_tags
    query.exclude_tags = exclude_tags
    query.ids = ids
    searched_posts = await posts.search(query)
    return JSONResponse(
        content=jsonable_encoder(searched_posts),
        headers={"Cache-Control": "max-age=60, public"},
    )
