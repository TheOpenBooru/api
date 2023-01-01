from . import router
from openbooru.modules import schemas, database, fastapi
from fastapi import Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache


@router.get("/autocomplete",
    response_model=list[schemas.Tag],
    dependencies=[
        Depends(fastapi.PermissionManager("canSearchTags")),
    ],
)
@cache(expire=3600,)
async def autocomplete_tags(
        text: str = Query(description="The start of a tag"),
        limit: int = Query(default=10, gt=0, le=100)
        ):
    query = schemas.TagQuery(name_like=text, limit=limit)
    try:
        tags = database.Tag.search(query)
    except TimeoutError:
        raise HTTPException(500, "The search timed out")
    
    return JSONResponse(
        content=jsonable_encoder(tags),
        headers={"Cache-Control": "max-age=300, public"},
    )
