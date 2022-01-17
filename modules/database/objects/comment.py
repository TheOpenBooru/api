from dataclasses import dataclass

from modules.database.objects import user
from . import _db_run,_combine_kwargs,_isUnique,Validate

_DATA_QUERY = """
"""

@dataclass(frozen=True)
class Comment:
    ...


def create() -> Comment:
    ...


def get(id:int=None) -> Comment:
    ...


def search(limit:int=10,**kwargs) -> list[Comment]:
    ...


def set(id:int,**kwargs):
    ...

def delete(id:int):
    ...
