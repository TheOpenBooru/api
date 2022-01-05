import os
from typing import Any
from .. import db_run,isUnique,isValid

def combine_kwargs(table:dict[str,list],values:dict[str,Any]) -> str:
    query = ""
    for key,value in values.items():
        if key not in table:
            raise ValueError("A kwarg key is invalid")
        elif not isinstance(value,table[key][0]):
            raise KeyError("A kwarg was not of the correct type")
        
        query += f" {table[key][1]} "
    
    return query


from .image import Image
from .tag import Tag
from .post import Post
from .user import User