from . import router
from cachetools import TTLCache, cached
from modules import schemas, database, fastapi
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/all",
    operation_id="all_tags",
    response_model=list[schemas.Tag],
    dependencies=[
        Depends(fastapi.PermissionManager("canRecieveAllTags")),
    ],
)
async def all_tags():
    return JSONResponse(
        content=cached_get_tags(),
        headers={"Cache-Control": "max-age=3600, public"},
    )


@cached(TTLCache(maxsize=1,ttl=60*60))
def cached_get_tags():
    tags = database.Tag.all()
    return jsonable_encoder(tags)
