from . import router
from modules import schemas, posts, account, database
from modules.fastapi.dependencies import DecodeToken, RequirePermission, RateLimit, RequireCaptcha
from fastapi import status, UploadFile, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/create",
    response_model=schemas.Post,
    responses= {
        400:{"description": "Failed To Create Post From Image"},
        401:{},
        403:{},
        409:{"description": "Post Already Exists"},
    },
    dependencies=[
        Depends(RequireCaptcha),
        Depends(RequirePermission("canCreatePosts")),
        Depends(RateLimit("3/minute")),
    ],
)
async def create_post(image:UploadFile, user:account.Account = Depends(DecodeToken)):
    try:
        data = await image.read()
        filename = image.filename
        post = await posts.create(data,filename,uploader_id=user.id)
    except posts.PostExistsException:
        return PlainTextResponse("Post Already Exists", 409)
    except Exception as e:
        return PlainTextResponse("Generic Error", 400)
    else:
        return JSONResponse(jsonable_encoder(post))