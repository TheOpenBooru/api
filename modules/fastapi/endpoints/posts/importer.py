from . import router
from modules import schemas, downloaders, database, posts
from modules.fastapi.dependencies import DecodeToken, RequirePermission
from fastapi import status, Depends, Body
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/import",
    operation_id="import_post",
    response_model=list[schemas.Post],
    responses= {
        400:{"description":"Post Creation Failure"},
        409:{"description":"Post already exists with that source"},
    },
    dependencies=[
        Depends(RequirePermission("canCreatePosts")),
    ],
)
async def import_url(url:str = Body(...), account:DecodeToken = Depends()):
    if database.Post.source_exists(url):
        return PlainTextResponse("Post already exists with that source", 409)
    
    try:
        new_posts = await downloaders.download_url(url)
    except downloaders.DownloadFailure as e:
        return PlainTextResponse(str(e), 400)
    except Exception:
        return PlainTextResponse("Failed to Import URL", 400)
    else:
        for post in new_posts:
            post.uploader = account.user_id
            posts.insert(post)
        
        return new_posts
