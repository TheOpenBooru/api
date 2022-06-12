from . import router
from modules import schemas, posts, settings
from typing import Union
from fastapi import Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/search",
    response_model=list[schemas.Post],
    status_code=200,
    responses={
        200:{"description":"Successfully Retrieved"},
    },
)
async def search_posts(
        index:int = Query(default=0, description="Offset by this many posts"),
        limit:int = Query(default=settings.POSTS_SEARCH_MAX_LIMIT,lt=settings.POSTS_SEARCH_MAX_LIMIT + 1, description="Maximum number of posts to return"),
        sort:schemas.Valid_Post_Sorts = Query(default=settings.POSTS_SEARCH_DEFAULT_SORT, description="The sort order for the posts"),
        descending:bool = Query(default=True, description="The sort order for the posts"),
        include_tags:list[str] = Query(default=[], description="Include posts with these tags"),
        exclude_tags:list[str] = Query(default=[], description="Exclude posts with these tags"),
        created_after:Union[float,None] = Query(default=None, description="Posts that were created after this unix timestamp"),
        created_before:Union[float,None] = Query(default=None, description="Posts that were created before this unix timestamp"),
        md5:Union[str,None] = Query(default=None, description="Posts with this md5"),
        sha256:Union[str,None] = Query(default=None, description="Posts with this sha256"),
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
