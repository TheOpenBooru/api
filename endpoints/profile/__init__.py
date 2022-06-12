from fastapi import APIRouter
router = APIRouter(prefix="/profile",tags=["Profile"])
from . import profile, settings
