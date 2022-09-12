from . import router
from modules import schemas, posts, account, database
from modules.fastapi.dependencies import DecodeToken, RequirePermission
from fastapi import status, UploadFile, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/create",
    operation_id="create_post",
    response_model=schemas.Post,
    responses= {
        400:{"description": "Failed To Create Post From Image"},
        409:{"description": "Post Already Exists"},
    },
    dependencies=[
        Depends(RequirePermission("canCreatePosts")),
    ],
)
async def create_post(image:UploadFile, account:DecodeToken = Depends()):
    try:
        data = await image.read()
        filename = image.filename
        post = await posts.create(data,filename,uploader_id=account.user_id)
    except posts.PostExistsException:
        return PlainTextResponse("Post Already Exists", 409)
    except Exception as e:
        return PlainTextResponse("Generic Error", 400)
    else:
        return JSONResponse(jsonable_encoder(post))