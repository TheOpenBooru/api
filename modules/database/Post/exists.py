from . import post_collection

def exists(id:int) -> bool:
    return _exists_by_filter({'id':id})

def md5_exists(md5:str) -> bool:
    return _exists_by_filter({"hashes.md5s":{'$elemMatch':{"$eq":md5}}})

def sha256_exists(sha256:str) -> bool:
    return _exists_by_filter({"hashes.sha256s":{'$elemMatch':{"$eq":sha256}}})

def source_exists(source:str) -> bool:
    return _exists_by_filter({"source":{'$elemMatch':{"$eq":source}}})

def _exists_by_filter(filter: dict) -> bool:
    document = post_collection.find_one(filter)
    return document != None
