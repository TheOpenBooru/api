from . import router
from modules import schemas,store
from fastapi import responses, status

@router.get('/image/{key}',response_model=bytes)
def get_image(key:str):
    CACHE_HEADER = {
        "Cache-Control": "max-age=31536000, public"
    }
    try:
        data = store.get(key)
    except FileNotFoundError:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return responses.Response(data,headers=CACHE_HEADER)