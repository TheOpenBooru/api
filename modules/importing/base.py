from modules.schemas import Post

class BaseImporter:
    name:str
    enabled:bool = False
    functional:bool = False
    def __init__(self):
        pass

    async def load_default(self):
        pass


class LocalImporter(BaseImporter):
    pass


class URLImporter(BaseImporter):
    def is_valid_url(self, url:str) -> bool:
        raise NotImplementedError
    
    async def download_url(self, url:str) -> list[Post]:
        raise NotImplementedError


class ImportFailure(Exception):
    pass
