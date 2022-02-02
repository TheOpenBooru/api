import yaml
from typing import Any
from cachetools import cached,TTLCache

@cached(cache=TTLCache(maxsize=128, ttl=30))
def get(setting:str) -> Any:
    """Raises:
    - KeyError: Invalid Setting Name
    """
    with open('./config.yml') as f:
        config = yaml.full_load(f)
    for key in setting.split('.'):
        try:
            config = config[key]
        except:
            raise KeyError(f'Invalid Setting: {setting}')
    return config