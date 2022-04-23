from modules import settings as _settings

if _settings.STORAGE_METHOD == "s3":
    from .aws import get,put,clear,delete,url
elif _settings.STORAGE_METHOD == "local":
    from .local import get,put,clear,delete,url
else:
    raise ValueError(f"Invalid storage method: {_settings.STORAGE_METHOD}")

from . import aws,local
