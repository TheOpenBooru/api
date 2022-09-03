from modules.schemas import Post
from typing import Union
from datetime import timedelta

class ImportFailure(Exception): pass

class Importer:
    enabled:bool = False
    functional:bool = False
    time_between_runs:Union[None, timedelta] = timedelta(days=1)
    def __init__(self):
        pass

    async def load(self, limit:Union[int, None] = None):
        raise NotImplementedError
