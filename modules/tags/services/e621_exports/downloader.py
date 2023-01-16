from . import parse_namespace_data, parse_parents_data, parse_siblings_data
from typing import Callable, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
import gzip
from pathlib import Path


@dataclass(frozen=False)
class Tag:
    tag:str
    namespace:Optional[str] = None
    siblings:Optional[list[str]] = None
    parents:Optional[list[str]] = None


def download_tag_data(tags:list[str]) -> dict[str, Tag]:
    types:list[tuple[str, str, Callable]] = [
        ("namespace", "tags", parse_namespace_data),
        ("parents", "tag_implications", parse_parents_data),
        ("siblings", "tag_aliases", parse_siblings_data),
    ]

    tag_lookup = {}
    for type, url_fragement, parser in types:
        url = _generate_url(url_fragement)
        text = _get_e621_data(type, url)
        _delete_previous_cache(type)
        lookup = parser(text, tags)
        
        for tag, value in lookup.items():
            if tag not in tag_lookup:
                tag_lookup[tag] = Tag(tag=tag)

            if type == "namespace":
                tag_lookup[tag].namespace = value
            elif type == "parents":
                tag_lookup[tag].parents = value
            elif type == "siblings":
                tag_lookup[tag].siblings = value

    
    return tag_lookup


def _generate_url(fragement:str) -> str:
    date = datetime.now()
    # Yesterdays date will always have a dump
    yesterdays_date = date + timedelta(days=-1)
    date_string = yesterdays_date.strftime("%Y-%m-%d")
    return f"https://e621.net/db_export/{fragement}-{date_string}.csv.gz"


def _get_e621_data(type:str, url: str):
    cached_path = _generate_cache_filename(type, datetime.now())
    
    if cached_path.exists():
        return cached_path.read_text()
    else:
        r = requests.get(url)
        data = gzip.decompress(r.content)
        text =  data.decode()
        cached_path.write_text(text)
        return text


def _delete_previous_cache(type:str):
    date = datetime.now()
    date -= timedelta(days=1)
    path = _generate_cache_filename(type, date)
    path.unlink(missing_ok=True)


def _generate_cache_filename(type:str, date: datetime) -> Path:
    date_string = date.strftime("%Y-%m-%d")
    filename = f"{type}-{date_string}.csv"
    return Path("./data/cache", filename)
