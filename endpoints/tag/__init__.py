from fastapi import APIRouter
router = APIRouter(prefix="/tags",tags=["Tag"])
from . import all,get