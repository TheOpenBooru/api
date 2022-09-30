from modules.normalise import normalise_tag
import csv


def parse_siblings_data(text:str, tags:list[str]) -> dict:
    lines = text.split('\n')
    reader = csv.reader(lines)
    tag_lookup: dict[str, list[str]] = {}
    
    next(reader) # Skip Initial Line
    for line in reader:
        try:
            sibling, tag = line[1:3]
            if tag not in tags:
                continue
            
            tag = normalise_tag(tag)
            sibling = normalise_tag(sibling)
            
            if tag not in tag_lookup:
                tag_lookup[tag] = []
            
            tag_lookup[tag].append(sibling)
        except Exception:
            continue

    for tag, siblings in list(tag_lookup.items()):
        for sibling in siblings:
            new_siblings = siblings.copy()
            new_siblings.append(tag)
            new_siblings.remove(sibling)
            tag_lookup[sibling] = new_siblings
    
    return tag_lookup
