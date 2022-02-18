from fastapi import APIRouter
router = APIRouter(prefix="/image",tags=["Image"])
from . import get