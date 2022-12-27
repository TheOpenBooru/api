from modules import normalise
import csv
from tqdm import tqdm


def parse_namespace_data(text:str, tags:list[str]) -> dict:
    tag_lookup = {}
    
    lines = text.split('\n')
    reader = csv.reader(lines)
    next(reader) # Skip Initial Line

    for line in tqdm(reader, desc="Parsing Namespace Data"):
        try:
            name, category = line[1:3]
            if name not in tags:
                continue
            else:
                tag = normalise.normalise_tag(name)
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
