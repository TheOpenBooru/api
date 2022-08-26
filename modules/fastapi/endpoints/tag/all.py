from . import router
from modules import schemas, database
from modules.fastapi.dependencies import RateLimit
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/all",
    operation_id="tag_all",
    response_model=list[schemas.Tag],
    status_code=200,
    responses={
        200:{"description":"Successfully Retrieved"},
    },
    dependencies=[
        Depends(RateLimit("2/day")),
    ],
)
async def all_tags():
    tags = database.Tag.all()
    return JSONResponse(
        content=jsonable_encoder(tags),
        headers={"Cache-Control": f"max-age={60*60*24}, public"},
    )
