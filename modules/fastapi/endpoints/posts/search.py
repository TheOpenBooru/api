from . import router
from modules import schemas, posts
from modules.fastapi.dependencies import PermissionManager
from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache


@router.get(
    path="/search",
    response_model=list[schemas.Post],
    dependencies=[
        Depends(PermissionManager("canSearchPosts")),
    ]
)
@cache(expire=60)
async def search_posts(
        query: schemas.PostQuery = Depends(),
        media_types: list[schemas.MediaType] = Query(default=[], description="Media Types to include"),
        ratings: list[schemas.Rating] = Query(default=[], description="Ratings to exclude from the results"),
        include_tags: list[str] = Query(default=[]),
        exclude_tags: list[str] = Query(default=[]),
        ids:list[int] = Query(default=[]),
        creators:list[int] = Query(default=[]),
        ):
    query.include_tags = include_tags
    query.exclude_tags = exclude_tags
    query.ids = ids
    query.creators = creators
    query.ratings = ratings
    query.media_types = media_types

    try:
        searched_posts = await posts.search(query)
    except TimeoutError:
        return Response("The Search Timed Out", 500)
    else:
        return JSONResponse(
            content=jsonable_encoder(searched_posts),
            headers={"Cache-Control": "max-age=300, public"},
        )
