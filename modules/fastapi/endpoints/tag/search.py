from . import router
from modules import schemas, database, fastapi
from fastapi import Depends, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache


@router.get("/search",
    response_model=list[schemas.Tag],
    dependencies=[
        Depends(fastapi.PermissionManager("canSearchTags")),
    ],
)
@cache(expire=3600)
async def search_tags(query:schemas.TagQuery = Depends()):
    try:
        tags = database.Tag.search(query)
    except TimeoutError:
        return Response(status_code=status.HTTP_504_GATEWAY_TIMEOUT)
    else:
        return JSONResponse(
            content=jsonable_encoder(tags),
            headers={"Cache-Control": "max-age=300, public"},
        )
