from fastapi import APIRouter
router = APIRouter(prefix='/posts')
from . import create,edit,get,delete,search