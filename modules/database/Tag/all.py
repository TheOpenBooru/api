from . import tag_collection,Tag

def all() -> list[Tag]:
    docs = tag_collection.find({})
    all_tags = [Tag.parse_obj(doc) for doc in docs]
    return all_tags
