from . import router
from modules import schemas, posts
from modules.fastapi.dependencies import DecodeToken, PermissionManager
from fastapi import UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/create",
    response_model=schemas.Post,
    responses= {
        400:{"description": "Failed To Create Post From Image"},
        409:{"description": "Post Already Exists"},
    },
    dependencies=[
        Depends(PermissionManager("canCreatePosts")),
    ],
)
async def create_post(image:UploadFile, account:DecodeToken = Depends()):
    try:
        data = await image.read()
        filename = image.filename
        post = await posts.create(data,filename,uploader_id=account.user_id)
    except posts.PostExistsException:
        raise HTTPException(409, "Post Already Exists")
    except Exception as e:
        raise HTTPException(400, "Generic Error")
    else:
        return JSONResponse(jsonable_encoder(post))