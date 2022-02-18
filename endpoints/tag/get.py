from . import router
from modules import schemas

@router.get('/tag/{name}',response_model=schemas.Tag,tags=["Unprivileged"])
def get_tag(name:str):
    ...