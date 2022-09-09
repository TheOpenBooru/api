from modules.schemas import Post

class Downloader:
    name:str
    enabled:bool = False
    functional:bool = True
    def __init__(self):
        pass

    def is_valid_url(self, url:str) -> bool:
        raise NotImplementedError
    
    async def download_url(self, url:str) -> list[Post]:
        raise NotImplementedError


class DownloadFailure(Exception):
    pass
