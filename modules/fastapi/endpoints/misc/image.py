from .. import router
from modules import store, settings
from fastapi import Response, status
from fastapi.responses import RedirectResponse, StreamingResponse


@router.get("/image/{file}",
    include_in_schema=False
)
def get_image(file:str):
    CACHE_HEADER = {
        "Cache-Control": "max-age=31536000, public"
    }
    if store.method.local == True:
        try:
            data = store.get(file)
        except FileNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return StreamingResponse(
                data,
                headers=CACHE_HEADER
            )
    else:
        url = store.url(file)
        return RedirectResponse(url=url)