from . import router
from modules import schemas,posts
from fastapi import Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@router.get("/search", response_model=list[schemas.Post])
async def search_posts(
        limit:int = Query(64),
        index:int = Query(0),
        include_tags:list[str] = Query([]),
        exclude_tags:list[str] = Query([]),
        ):
    query = schemas.Post_Query(
        limit=limit,
        index=index,
        include_tags=include_tags,
        exclude_tags=exclude_tags
    )
    
    searched_posts = await posts.search(query)
    return JSONResponse(
        content=jsonable_encoder(searched_posts),
        headers={"Cache-Control": "max-age=60, public"},
    )
