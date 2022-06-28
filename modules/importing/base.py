class BaseImporter:
    name:str
    enabled:bool = False
    functional:bool = False
    def __init__(self):
        ...

    async def import_default(self):
        raise NotImplementedError

class LocalImporter(BaseImporter):
    pass


class URLImporter(BaseImporter):
    def is_valid_url(self, url:str) -> bool:
        raise NotImplementedError
    
    async def import_url(self, url:str):
        raise NotImplementedError


class ImportFailure(Exception):
    pass
