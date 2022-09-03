from datetime import datetime, timedelta
from modules.normalisation import normalise_tag
import requests
import gzip
import json
from pathlib import Path
import csv

tag = str
namespace = str
def download_namespace_data() -> dict[tag, namespace]:
    url = _generate_url()
    r = requests.get(url)
    data = gzip.decompress(r.content)
    text = data.decode()
    namespace_data = _parse_csv(text)
    return namespace_data


def _generate_url():
    date = datetime.now()
    yesterdays_date = date - timedelta(days=1) # Yesterdays date will always have a 
    date_string = yesterdays_date.strftime("%Y-%m-%d")
    url = f"https://e621.net/db_export/tags-{date_string}.csv.gz"
    return url


def _parse_csv(text:str) -> dict:
    tag_lookup = {}
    
    lines = text.split('\n')
    reader = csv.reader(lines)
    next(reader) # Skip Initial Line
    
    for line in reader:
        try:
            _, name, category, _ = line
            tag = normalise_tag(name)
            namespace = _parse_category_id(category)
        except Exception:
            continue
        else:
            tag_lookup[tag] = namespace
    
    return tag_lookup


def _parse_category_id(id:str) -> str:
    namespaces = {
        "0": "generic",
        "1": "creator",
        "3": "copyright",
        "4": "character",
        "5": "species",
        "6": "invalid",
        "7": "meta",
        "8": "lore",
    }
    return namespaces[id]