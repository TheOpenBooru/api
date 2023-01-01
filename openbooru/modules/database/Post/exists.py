from . import post_collection


def exists(*,
        id: int|None = None,
        sources: list[str]|None = [],
        md5s: list[bytes] |None= [],
        sha256s:list[bytes]|None = [],
        phashes: list[bytes]|None = [],
    ):
    filters = []
    if id:
        filters.append({"id":{"$eq":id}})
    if sources:
        filters.append({"hashes.sources":{'$elemMatch':{"$in":sources}}})
    if md5s:
        filters.append({"hashes.md5s":{'$elemMatch':{"$in":md5s}}})
    if sha256s:
        filters.append({"hashes.sha256s":{'$elemMatch':{"$in":sha256s}}})
    if phashes:
        filters.append({"hashes.phashes":{'$elemMatch':{"$in":phashes}}})


    if filters:
        return _exists_by_filter({"$or": filters})
    else:
        raise ValueError("No Filters Specified")


def _exists_by_filter(filter: dict) -> bool:
    document = post_collection.find_one(filter)
    return document != None
