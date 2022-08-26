from typing import Union
from modules.schemas import Post

class ImportFailure(Exception): pass

class Importer:
    enabled:bool = False
    functional:bool = False
    def __init__(self):
        pass

    async def load(self, limit:Union[int, None] = None):
        raise NotImplementedError
