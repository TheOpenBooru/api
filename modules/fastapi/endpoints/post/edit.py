from . import router
from modules import schemas, posts, fastapi, account
from fastapi import Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Union


@router.patch('/post/{id}',
    responses={
        202:{"description":"Not Implemented"},
        404:{"description":"The Post Could Not Be Found"},
    },
    response_model=schemas.Post,
    dependencies=[Depends(fastapi.RequirePermission("canEditPosts"))],
)
async def edit_post(
        id:int,
        tags:Union[None,list[str]] = Body(default=None,description="The tags for the new post version"),
        source:Union[None,str] = Body(default=None,description="The source to update the post with"),
        user:account.Account = Depends(fastapi.DecodeToken)
        ):
    try:
        new_post = posts.editPost(id, user.id, tags, source)
    except posts.PostEditFailure as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    else:
        return JSONResponse(
            content=jsonable_encoder(new_post)
            status_code=202,
        )
