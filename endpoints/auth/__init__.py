from fastapi import APIRouter
router = APIRouter(prefix="/auth",tags=["Auth"])
from . import login,register