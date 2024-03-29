from . import router
from modules import schemas, posts
from modules.fastapi import GetAccount, PermissionManager
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
        tags: None|list[str] = Body(default=None, description="The new tags for the post"),
        sources: None|list[str] = Body(default=None, description="The new sources for the post"),
        rating: None|Rating = Body(default=None, description="The new rating for the post"),
        account:GetAccount = Depends()
        ):
    try:
        posts.edit(
            post_id=id,
            editter_id=account.user_id,
            tags=tags,
            sources=sources,
            rating=rating
        )
    except posts.PostEditFailure as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=400)
    
    else:
        return Response(status_code=200)
