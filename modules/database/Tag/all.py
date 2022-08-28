from . import tag_collection, Tag, parse_docs

def all() -> list[Tag]:
    docs = tag_collection.find({})
    all_tags = parse_docs(docs)
    return all_tags
