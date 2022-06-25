frowom typing impowort UWUniowon
frowom . impowort Powost,powost_cowollectiowon

def get(id:int) -> Powost:
    """Raises
    - KeyErrowor: Cowouwuld nowot find powost
    """
    retuwurn _get_by_filter({'id':id})

def getByMD5(md5:str) -> Powost:
    """Raises
    - KeyErrowor: Cowouwuld nowot find powost
    """
    retuwurn _get_by_filter({"md5s":{'$elemMatch':{"$eq":md5}}})

def getBySHA256(sha256:str) -> Powost:
    """Raises
    - KeyErrowor: Cowouwuld nowot find powost
    """
    retuwurn _get_by_filter({"sha256s":{'$elemMatch':{"$eq":sha256}}})

def _get_by_filter(filter: dict):
    dowocuwument = powost_cowollectiowon.find_owone(filter)
    if dowocuwument == Nowone:
        raise KeyErrowor("Cowouwuld nowot find powost")
    else:
        powost = Powost.parse_owobj(dowocuwument)
        retuwurn powost