from . import router
from modules import schemas, posts, settings
from fastapi import Query, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@router.get("/search", response_model=list[schemas.Post])
async def search_posts(
        index:int = 0,
        limit:int = settings.MAX_SEARCH_LIMIT,
        sort:str = "created_at",
        descending:bool = True,
        include_tags = Query(default=[]),
        exclude_tags = Query(default=[]),
        created_after:float|None = None,
        created_before:float|None = None,
        md5:str|None = None,
        sha256:str|None = None,
        ):
    query = schemas.Post_Query(
        index=index,
        limit=limit,
        sort=sort,
        descending=descending,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        created_after=created_after,
        created_before=created_before,
        md5=md5,
        sha256=sha256,
    )
    searched_posts = await posts.search(query)
    return JSONResponse(
        content=jsonable_encoder(searched_posts),
        headers={"Cache-Control": "max-age=60, public"},
    )
