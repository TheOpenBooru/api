from modules import settings as _settings

# if _settings.STORAGE_USE_AWS:
#     from .aws import get,put,clear,delete,url
# else:
    # from .local import get,put,clear,delete,url
# from . import aws,local

from .local import get,put,clear,delete,url
from . import local
