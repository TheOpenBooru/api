import yaml
from typing import Any
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=1, ttl=10))
def _load_config() -> dict:
    with open("./config.yml") as f:
        config = yaml.full_load(f)
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
