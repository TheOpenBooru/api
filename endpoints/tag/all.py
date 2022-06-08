from . import router
from modules import schemas, database
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

responses = {
    200:{"description":"Successfully Retrieved"},
}

@router.get("/all",
    response_model=list[schemas.Tag],
    status_code=200,
    responses=responses, # type: ignore
)
async def all_tags():
    tags = database.Tag.all()
    return JSONResponse(
        content=jsonable_encoder(tags),
        headers={"Cache-Control": "max-age=3600, public"},
    )
