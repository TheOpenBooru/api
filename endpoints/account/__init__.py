from fastapi import APIRouter
router = APIRouter(prefix="/account",tags=["Account"])
from . import login,register,profile