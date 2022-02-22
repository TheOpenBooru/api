from . import router
from modules import schemas,store
from fastapi import responses

@router.get('/get/{key}',response_model=bytes)
def get_image(key:str):
    return responses.Response(store.get(key))