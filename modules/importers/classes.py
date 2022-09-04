from modules.schemas import Post
from typing import Union
from datetime import timedelta

class ImportFailure(Exception): pass

class Importer:
    enabled:bool = False
    functional:bool = False
    time_between_runs:Union[None, float] = None
    def __init__(self):
        pass

    async def load(self, limit:Union[int, None] = None):
        raise NotImplementedError
