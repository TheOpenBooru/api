from . import router
from modules import schemas,posts
from fastapi import Response,status,UploadFile

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
async def create_post(data:bytes,filename:str):
    authorised = False
    if not authorised:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            post = await posts.create(data,filename) # type: ignore
        except Exception:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content="Failed to Create Post",
            )
        else:
            return post