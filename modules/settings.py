import yaml
from typing import Any
from cachetools import cached, TTLCache

_last_valid_config:dict = {}
@cached(cache=TTLCache(maxsize=1, ttl=5))
def _load_config() -> dict:
    global _last_valid_config
    try:
        with open("./config.yml") as f:
            config = yaml.full_load(f)
    except Exception:
        config = _last_valid_config
        return _last_valid_config
    else:
        _last_valid_config = config
        return config
    


@cached(cache=TTLCache(maxsize=1024, ttl=5))
def get(setting: str) -> Any:
    """Raises:
    - KeyError: Invalid Setting Name
    """
    config = _load_config()
    for key in setting.split("."):
        try:
            config = config[key]
        except:
            raise KeyError(f"Invalid Setting: {setting}")
    return config
