import os
from typing import Any
from .. import _db_run,Validate
from .. import isUnique as _isUnique

def _combine_kwargs(table:dict[str,str],values:dict[str,Any]) -> str:
    query = ""
    for key,value in values.items():
        query += f" {value} "
    return query


from . import comment, image, post, tag, user