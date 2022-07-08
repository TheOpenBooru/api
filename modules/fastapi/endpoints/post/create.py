from . import router
from modules import schemas, posts, account
from modules.fastapi.dependencies import DecodeToken, RequirePermission, RateLimit
from fastapi import status, UploadFile, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/create",
    response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED,
    responses= {
        201:{"description":"Successfully Created"},
        400:{"description":"Failed To Create Post From Image"},
        401:{"description":"Authorization Failure"},
        409:{"description":"Post Already Exists"},
    },
    dependencies=[
        Depends(RequirePermission("canCreatePosts")),
        Depends(RateLimit("3/minute")),
    ],
)
async def create_post(image:UploadFile, user:account.Account = Depends(DecodeToken)):
    try:
        data = await image.read()
        filename = image.filename
        post = await posts.create(data,filename,user_id=user.id)
    except posts.PostExistsException:
        return PlainTextResponse("Post Already Exists", 409)
    except Exception as e:
        return PlainTextResponse("Generic Error", 400)
    else:
        json = jsonable_encoder(post)
        return JSONResponse(json,201)