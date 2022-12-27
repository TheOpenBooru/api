from typing import Union
from modules import settings as _settings
from .base import BaseStore
from .s3 import S3Store
from .local import LocalStore


method: Union[S3Store, LocalStore]
if _settings.STORAGE_METHOD == 'local':
    method = LocalStore()
elif _settings.STORAGE_METHOD == 's3':
    method = S3Store()
else:
    raise RuntimeError("Invalid store method in settings.yml")


if method.usable == False:
    raise RuntimeError(f"Store Won't Work, Reason: '{method.fail_reason}'")

get = method.get
put = method.put
url = method.url
delete = method.delete
clear = method.clear

if _settings.WIPE_ON_STARTUP:
    clear()


def generate_generic_url(filename:str) -> str:
    return f"/media/{filename}"


def to_absolute_url(url: str) -> str:
    if not url.startswith("/"):
        return url
    else:
        return get_hostname() + url


def get_hostname():
    hostname, port = _settings.HOSTNAME, _settings.PORT
    if not _settings.SSL_ENABLED:
        if port == 80:
            return f"http://{hostname}"
        else:
            return f"http://{hostname}:{port}"
    else:
        if port == 443:
            return f"https://{hostname}"
        else:
            return f"https://{hostname}:{port}"
