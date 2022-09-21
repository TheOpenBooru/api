from . import router
from modules import schemas, database, fastapi, tags
from fastapi import Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.post("/edit",
    operation_id="edit_tag",
    response_model=schemas.Tag,
    dependencies=[
        Depends(fastapi.RequirePermission("canEditTags")),
    ],
)
async def edit_tag(
        tag:str,
        namespace:str|None = Body(default=None),
        parents:list[str]|None = Body(default=None),
        siblings:list[str]|None = Body(default=None),
    ):
    new_tag = await tags.edit(tag, namespace, parents, siblings)
    return new_tag
