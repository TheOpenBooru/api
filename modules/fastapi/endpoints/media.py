from . import router
from pathlib import Path
from typing import Union
from modules import store
from modules.importers.utils import guess_mimetype
from fastapi import Response, status, Header, HTTPException
from fastapi.responses import RedirectResponse, FileResponse


@router.get("/media/{filename}",
    include_in_schema=False
)
async def get_media(filename:str, range:Union[str, None] = Header(None)):
    CACHE_HEADER = { "Cache-Control": "max-age=31536000, public, immutable"}

    if not isinstance(store.method,store.LocalStore):
        url = store.url(filename)
        return RedirectResponse(url=url,status_code=308)
    else:
        try:
            path = Path(store.method.path(filename))
        except FileNotFoundError:
            raise HTTPException(404)

        if range == None:
            return FileResponse(path,headers=CACHE_HEADER)
        else:
            start, end = range.replace("bytes=", "").split("-")
            start = int(start)
            end = int(end) if end else start + (1024 * 1024)
            
            with open(path, "rb") as video:
                video.seek(start)
                data = video.read(end - start)
            
            filesize = str(path.stat().st_size)
            headers = {
                'Content-Range': f'bytes {start}-{end}/{filesize}',
                'Accept-Ranges': 'bytes',
                **CACHE_HEADER
            }
            mime = guess_mimetype(str(path))
            return Response(
                data,
                status_code=206,
                headers=headers,
                media_type=mime
            )