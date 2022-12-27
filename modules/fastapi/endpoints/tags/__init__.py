from fastapi import APIRouter
router = APIRouter(prefix="/tags",tags=["Tag"])
from . import search, autocomplete, all, edit, get