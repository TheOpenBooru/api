import logging
from . import router
from modules import schemas, posts, database
from endpoints.meta.token import Account,DecodeToken
from fastapi import Response, status, Depends, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

responses = {
    201:{"description":"Successfully Created"},
    400:{"description":"Failed To Create Post From Image"},
    401:{"description":"You Are Not Authorised To Create A Post"},
}

@router.post("/create",
    response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED,
    responses=responses, # type: ignore
)

async def create_post(image_file:UploadFile, user:Account=Depends(DecodeToken)):
    if not user.permissions.canCreatePosts:
        return Response(status_code=401)
    
    try:
        data = await image_file.read()
        filename = image_file.filename
        post = await posts.create(data,filename) # type: ignore
        database.User.createPost(user.id,post.id)
    except Exception as e:
        logging.debug(e)
        return Response(status_code=400)
    else:
        json = jsonable_encoder(post)
        return JSONResponse(json,201)