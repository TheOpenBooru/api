import yaml
from typing import Any
from cachetools import cached, TTLCache

_last_valid_config:dict|None = None
@cached(cache=TTLCache(maxsize=1, ttl=5))
def _load_config() -> dict:
    global _last_valid_config
    try:
        with open("./config.yml") as f:
            config = yaml.full_load(f)
    except Exception as e:
        if _last_valid_config is None:
            raise ValueError("Invalid config.yml")
        else:
            print(f"Failed to load settings, using last valid")
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
        if key not in config:
            raise KeyError(f"Invalid Setting: {setting}")
        else:
            config = config[key]
    return config
