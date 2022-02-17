from . import router
from modules import schemas

@router.get('/get',response_model=schemas.Tag,tags=["Unprivileged"])
def get_tag(name:str):
    ...