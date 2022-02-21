from . import router
from modules import schemas,store

@router.get('/get/{key}',response_model=bytes,tags=["Unprivileged"])
def get_image(key:str) -> bytes:
    return store.get(key)