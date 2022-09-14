from . import post_collection


def exists(id:int) -> bool:
    return _exists_by_filter({'id':id})


def md5_exists(md5:bytes) -> bool:
    return _exists_by_filter({"hashes.md5s":{'$elemMatch':{"$eq":md5}}})


def sha256_exists(sha256:bytes) -> bool:
    return _exists_by_filter({"hashes.sha256s":{'$elemMatch':{"$eq":sha256}}})


def source_exists(source:str) -> bool:
    # return _exists_by_filter({"source":{'$elemMatch':{"$eq":source}}})
    return _exists_by_filter({"source": source})


def phash_exists(phash:bytes) -> bool:
    """Raises
    - KeyError: Could not find post
    """
    return _exists_by_filter({"hashes.phashes":{'$elemMatch':{"$eq":phash}}})


def _exists_by_filter(filter: dict) -> bool:
    document = post_collection.find_one(filter)
    return document != None
