from . import router
from modules import schemas, database
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/all",
    response_model=list[schemas.Tag],
    status_code=200,
    responses={
        200:{"description":"Successfully Retrieved"},
    },
)
async def all_tags():
    tags = database.Tag.all()
    return JSONResponse(
        content=jsonable_encoder(tags),
        headers={"Cache-Control": f"max-age={60*60*24}, public"},
    )
