from .. import router
from modules import store, settings
from fastapi import Response, responses, status

@router.get('/image/{file}',status_code=200,include_in_schema=False)
def get_image(file:str):
    CACHE_HEADER = {
        "Cache-Control": "max-age=31536000, public"
    }
    if settings.STORAGE_METHOD == "local":
        try:
            data = store.get(file)
        except FileNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data,headers=CACHE_HEADER)
    else:
        url = store.url(file)
        return responses.RedirectResponse(url=url)