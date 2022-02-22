from . import router
from modules import schemas,store
from fastapi import responses, status

@router.get('/get/{key}',response_model=bytes)
def get_image(key:str):
    try:
        data = store.get(key)
    except KeyError:
        return responses.Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return responses.Response(data)