from fastapi import APIRouter
router = APIRouter(prefix="/misc",tags=["Misc"])
from . import status,image