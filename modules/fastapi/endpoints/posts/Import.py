from . import router
from modules import schemas, downloaders, database, posts
from modules.fastapi.dependencies import DecodeToken, PermissionManager
from fastapi import Depends, Body, HTTPException
from fastapi.responses import PlainTextResponse


@router.post("/import",
    operation_id="import_post",
    response_model=list[schemas.Post],
    responses= {
        400:{"description":"Post Creation Failure"},
        409:{"description":"Post already exists with that source"},
    },
    dependencies=[
        Depends(PermissionManager("canCreatePosts")),
    ],
)
async def import_url(url:str = Body(...), account:DecodeToken = Depends()):
    try:
        new_posts = await posts.Import(url, account.user_id)
    except posts.PostImportFailure as e:
        raise HTTPException(400, e.message)
    except Exception:
        raise HTTPException(400, "Unknown Error")
    else:
        return new_posts
