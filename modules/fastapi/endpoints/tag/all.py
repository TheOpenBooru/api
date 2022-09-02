from . import router
from cachetools import TTLCache, cached
from modules import schemas, database
from modules.fastapi.dependencies import RateLimit
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json


@router.get("/all",
    response_model=list[schemas.Tag],
    dependencies=[
        Depends(RateLimit("1/second")),
    ],
)
async def all_tags():
    data = get_data()
    return JSONResponse(
        content=data,
        headers={"Cache-Control": "max-age=3600, public"},
    )


@cached(TTLCache(maxsize=1,ttl=60*60))
def get_data():
    tags = database.Tag.all()
    return jsonable_encoder(tags)
