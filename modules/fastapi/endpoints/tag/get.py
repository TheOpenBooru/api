from . import router
from modules import schemas, database, fastapi, tags
from fastapi import Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/get",
    operation_id="get_tag",
    response_model=schemas.Tag,
    responses={
        404: { "description": "Tag Does Not Exist"}
    },
    dependencies=[
        Depends(fastapi.PermissionManager("canSearchTags")),
    ],
)
async def get_tag(tag:str):
    try:
        tag_data = database.Tag.get(tag)
    except KeyError:
        raise HTTPException(404, "Tag Does Not Exist")
    else:
        return tag_data
