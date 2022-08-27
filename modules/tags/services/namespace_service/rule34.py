from dataclasses import dataclass
from functools import cache
from pprint import pprint
import re
from typing import Union
import requests


@cache
def get_rule34_namespace(tag:str) -> Union[str,None]:
    tags = _tag_autocomplete(tag)
    for r34_tag in tags:
        if r34_tag.name == tag:
            return r34_tag.type
    return None


@dataclass
class Tag:
    name:str
    count:int
    type:str


def _tag_autocomplete(search:str) -> list[Tag]:
    r = requests.get(
        "https://rule34.xxx/public/autocomplete.php",
        params={
            "q":search
        }
    )
    data = r.json()
    
    TYPE_CONVERSION = {
        "general":"generic",
        "metadata":"meta",
        "artist":"creator",
        "character":"character",
        "copyright":"copyright",
    }
    
    tags = []
    for tag_data in data:
        name = tag_data["value"]
        if tag_data["type"] in TYPE_CONVERSION:
            type = TYPE_CONVERSION[tag_data["type"]]
        else:
            type = tag_data["type"]
        
        count_match = re.search(r"[0-9]+",tag_data["label"])
        count = int(count_match.group())
        if type not in set(TYPE_CONVERSION.values()):
            breakpoint()

        tag = Tag(
            name=name,
            type=type,
            count=count,
        )
        tags.append(tag)
    
    return tags