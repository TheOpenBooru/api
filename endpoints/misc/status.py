from . import router
from modules import schemas,settings

@router.get('/status',response_model=schemas.misc.Status)
def get_status():
    return {
        "online": True,
        "config": {
            "DefaultSort":settings.POSTS_SEARCH_DEFAULT_SORT,
            "SearchLimit":settings.POSTS_SEARCH_MAX_LIMIT,
            "SiteName":settings.SITE_NAME,
            "Hostname":settings.HOSTNAME,
            "Port":settings.PORT,
        }
    }
