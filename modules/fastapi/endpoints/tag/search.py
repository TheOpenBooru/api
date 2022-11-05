from . import router
from modules import schemas, database, fastapi
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/search",
    response_model=list[schemas.Tag],
    dependencies=[
        Depends(fastapi.PermissionManager("canSearchTags")),
    ],
)
async def search_tags(query:schemas.TagQuery = Depends()):
    tags = database.Tag.search(query)
    return JSONResponse(
        content=jsonable_encoder(tags),
        headers={"Cache-Control": "max-age=300, public"},
    )
