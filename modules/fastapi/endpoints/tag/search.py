from . import router
from modules import schemas, database
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/search",
    operation_id="tag_search",
    response_model=list[schemas.Tag],
    status_code=200,
    responses={
        200:{"description":"Successfully Retrieved"},
    },
)
async def search_tags(query:schemas.Tag_Query = Depends()):
    tags = database.Tag.search(query)
    return JSONResponse(
        content=jsonable_encoder(tags),
        headers={"Cache-Control": "max-age=3600, public"},
    )
