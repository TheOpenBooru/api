from . import router
from modules import schemas

@router.get('/all',response_model=list[schemas.Tag],tags=["Unprivileged"])
def list_tags():
    ...