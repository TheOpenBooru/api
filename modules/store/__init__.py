from modules import settings as _settings
from .base import BaseStore
from .s3 import S3Store
from .local import LocalStore


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
    hostname = _settings.HOSTNAME
    port = _settings.PORT
    if port == 80:
        return f"http://{hostname}/image/{filename}"
    elif port == 443:
        return f"https://{hostname}/image/{filename}"
    elif _settings.SSL_ENABLED:
        return f"https://{hostname}:{port}/image/{filename}"
    else:
        return f"http://{hostname}:{port}/image/{filename}"
