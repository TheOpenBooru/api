from . import router
from modules import store
from fastapi import Response, status
from fastapi.responses import RedirectResponse, FileResponse


@router.get("/media/{filename}",
    include_in_schema=False
)
def get_media(filename:str):
    CACHE_HEADER = {
        "Cache-Control": "max-age=31536000, public"
    }
    if isinstance(store.method,store.LocalStore):
        try:
            path = store.method.path(filename)
        except FileNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return FileResponse(path,headers=CACHE_HEADER)
    else:
        url = store.url(filename)
        return RedirectResponse(url=url,status_code=309)