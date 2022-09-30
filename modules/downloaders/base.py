from modules import errors, schemas

class Downloader:
    name:str
    enabled:bool = False
    def __init__(self):
        pass

    def is_valid_url(self, url:str) -> bool:
        raise NotImplementedError
    
    async def download_url(self, url:str) -> list[schemas.Post]:
        raise NotImplementedError


class DownloadFailure(errors.UserViewableException): pass
