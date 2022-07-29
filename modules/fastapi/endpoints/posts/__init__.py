from fastapi import APIRouter
router = APIRouter(prefix="/posts",tags=["Posts"])
from . import create, search, importer