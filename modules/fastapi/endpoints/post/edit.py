from . import router
from modules import schemas, posts
from modules.fastapi import DecodeToken, PermissionManager
from modules.schemas import Rating
from fastapi import Depends, Body, HTTPException, Response
from typing import Union
import logging


@router.patch('/{id}',
    response_model=schemas.Post,
    dependencies=[
        Depends(PermissionManager("canEditPosts")),
    ],
    responses={
        400:{"description":"Post Edit Failure"},
    }
)
async def edit_post(
        id:int,
        tags:Union[None,list[str]] = Body(default=None,description="The new tags for the post"),
        source:Union[None,str] = Body(default=None,description="The new source to update the post with"),
        rating:Union[None,Rating] = Body(default=None,description="The new rating for the post"),
        account:DecodeToken = Depends()
        ):
    try:
        posts.edit_post(
            post_id=id,
            editter_id=account.user_id,
            tags=tags,
            source=source,
            rating=rating
        )
    except posts.PostEditFailure as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=400)
    
    else:
        return Response(status_code=200)
