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
async def get_media(filename:str, range: str|None = Header(None)):
    CACHE_HEADER = { "Cache-Control": "max-age=31536000, public, immutable"}

    if not isinstance(store.method,store.LocalStore):
        url = store.url(filename)
        return RedirectResponse(url=url,status_code=308)

    path = store.method.path(filename)
    
    if not path.exists() or path.name == ".gitignore":
        raise HTTPException(404)
    
    if path.parent != Path("./data/storage"):
        raise HTTPException(404) # Path Traversal

    if range == None:
        return FileResponse(
            path,
            headers=CACHE_HEADER,
            media_type=guess_mimetype(str(path))
        )
    
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + (1024 ** 2)
    
    with open(path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
    
    headers = {
        'Content-Range': f'bytes {start}-{end}/{path.stat().st_size}',
        'Accept-Ranges': 'bytes',
        **CACHE_HEADER
    }
    return Response(
        data,
        status_code=206,
        headers=headers,
        media_type="video/mp4"
    )