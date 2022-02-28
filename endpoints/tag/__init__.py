from fastapi import APIRouter
router = APIRouter(prefix="/tag",tags=["Tag"])
from . import all