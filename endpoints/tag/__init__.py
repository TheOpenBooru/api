from fastapi import APIRouter
router = APIRouter(prefix='/posts')
from . import all,get