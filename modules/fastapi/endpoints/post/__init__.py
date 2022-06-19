from fastapi import APIRouter
router = APIRouter(prefix="/posts",tags=["Post"])
from . import create,edit,get,delete,search