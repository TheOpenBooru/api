from modules import schemas, errors
from typing import Union
from datetime import datetime

class DownloadFailure(errors.UserViewableException): pass


class Importer:
    enabled:bool = False
    time_between_runs:Union[None, float] = None
    def __init__(self):
        pass

    async def load(self, limit: Union[int, None] = None):
        raise NotImplementedError


class Downloader:
    def __init__(self):
        pass

    def is_valid_url(self, url:str) -> bool:
        raise NotImplementedError
    
    async def download_url(self, url:str) -> list[schemas.Post]:
        raise NotImplementedError


class Subscriber:
    def __init__(self):
        pass

    def is_valid_url(self, url:str) -> bool:
        raise NotImplementedError
    
    async def download_url(self, url:str) -> list[schemas.Post]:
        raise NotImplementedError

    def discover_urls(self, url: str, since: datetime = datetime.min) -> list[schemas.Post]:
        raise NotImplementedError
