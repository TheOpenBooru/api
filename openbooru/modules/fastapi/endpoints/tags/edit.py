from . import router
from openbooru.modules import schemas, database, fastapi, tags
from fastapi import Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.post("/edit",
    response_model=schemas.Tag,
    responses={
        400: { "description": "Post Not Found"}
    },
    dependencies=[
        Depends(fastapi.PermissionManager("canEditTags")),
    ],
)
async def edit_tag(
        tag:str,
        namespace:str|None = Body(default=None),
        parents:list[str]|None = Body(default=None),
        siblings:list[str]|None = Body(default=None),
    ):
    try:
        new_tag = await tags.edit(tag, namespace, parents, siblings)
    except tags.TagEditFailure as e:
        raise HTTPException(400, e.message)
    else:
        return new_tag
