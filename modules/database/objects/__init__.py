import os
from typing import Any
from .. import _db_run,Validate
from .. import isUnique as _isUnique

def _combine_kwargs(table:dict[str,list],values:dict[str,Any]) -> str:
    query = ""
    for key,value in values.items():
        if key not in table:
            raise ValueError("A kwarg key is invalid")
        elif not isinstance(value,table[key][0]):
            raise KeyError("A kwarg was not of the correct type")
        
        query += f" {table[key][1]} "
    
    return query


from . import Tag,Image,User,Post,Comment