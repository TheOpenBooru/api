from . import router

@router.get('/status',response_model=dict)
def get_status():
    return {
        "version": "0.0.1",
        "status": True
    }