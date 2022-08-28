from . import Tag, tag_collection, parse_doc

def get(name:str) -> Tag:
    """Raises
    - KeyError: Tag does not exist
    """
    document = tag_collection.find_one({'name':name})
    if document == None:
        raise KeyError(f'Tag does not exist')
    else:
        tag = parse_doc(document)
        return tag
