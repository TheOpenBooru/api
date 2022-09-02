from . import router
from modules import schemas, posts, account
from modules.fastapi.dependencies import DecodeToken, RequirePermission, RateLimit, RequireCaptcha
from modules.schemas import Ratings

from fastapi import Depends, Body, HTTPException, Response
from typing import Union


@router.patch('/{id}',
    response_model=schemas.Post,
    dependencies=[
        Depends(RequireCaptcha),
        Depends(RequirePermission("canEditPosts")),
        Depends(RateLimit("10/minute")),
    ],
)
async def edit_post(
        id:int,
        tags:Union[None,list[str]] = Body(default=None,description="The new tags for the post"),
        source:Union[None,str] = Body(default=None,description="The new source to update the post with"),
        rating:Union[None,Ratings] = Body(default=None,description="The new rating for the post"),
        user:account.Account = Depends(DecodeToken)
        ):
    try:
        posts.edit_post(
            post_id=id,
            editter_id=user.id,
            tags=tags,
            source=source,
            rating=rating
        )
    except posts.PostEditFailure as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return Response(status_code=200)
