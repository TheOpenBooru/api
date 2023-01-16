from modules.normalise import normalise_tag
import csv


def parse_parents_data(text:str, tags:list[str]) -> dict:
    lines = text.split('\n')
    reader = csv.reader(lines)
    tag_lookup: dict[str, list[str]] = {}
    
    next(reader) # Skip Initial Line
    for line in reader:
        ...

    return {}