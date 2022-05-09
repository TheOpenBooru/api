from . import router
from modules import schemas

@router.get('/status',response_model=schemas.misc.Status)
def get_status():
    return {
        "online": True
    }