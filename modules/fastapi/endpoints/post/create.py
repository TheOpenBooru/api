from . import router
from modules import schemas, posts, account, fastapi
from fastapi import Response, status, UploadFile, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.post("/create",
    response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED,
    responses= {
        201:{"description":"Successfully Created"},
        400:{"description":"Failed To Create Post From Image"},
        409:{"description":"Post Already Exists"},
    },
    dependencies=[Depends(fastapi.RequirePermission("canCreatePosts"))],
)
async def create_post(image:UploadFile, user:account.Account = Depends(fastapi.DecodeToken)):
    try:
        data = await image.read()
        filename = image.filename
        post = await posts.create(data,filename,user_id=user.id)
    except posts.PostExistsException:
        return Response("Post Already Exists", 409)
    except Exception as e:
        return Response("Generic Error", 400)
    else:
        json = jsonable_encoder(post)
        return JSONResponse(json,201)