from typing import Union
from . import user_collection

def exists(id:int) -> bool:
    return _exists_by_filter({"id":id})

def existsByUsername(username:str) -> bool:
    return _exists_by_filter({"username":username})

def existsByEmail(email:Union[str, None]) -> bool:
    return _exists_by_filter({"email":email})

def _exists_by_filter(filter:dict):
    document = user_collection.find_one(filter)
    return bool(document)
