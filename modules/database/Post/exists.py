from . import post_collection

def getByID(id:int) -> bool:
    """Raises
    - KeyError: Could not find post
    """
    return _exists_by_filter({'id':id})

def getByMD5(md5:str) -> bool:
    """Raises
    - KeyError: Could not find post
    """
    return _exists_by_filter({"hashes":{"md5s":{'$elemMatch':{"$eq":md5}}}})

def getBySHA256(sha256:str) -> bool:
    """Raises
    - KeyError: Could not find post
    """
    return _exists_by_filter({"hashes":{"sha256s":{'$elemMatch':{"$eq":sha256}}}})

def _exists_by_filter(filter: dict) -> bool:
    document = post_collection.find_one(filter)
    return document != None
