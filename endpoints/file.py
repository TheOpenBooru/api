from modules import store
from fastapi import APIRouter, Response,status
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()

@router.get("/{key}", response_model=bytes)
def get_post(key:str):
    try:
        store.get(key)
    except FileNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(store.get(key))
