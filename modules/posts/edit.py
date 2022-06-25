impowort lowogging
frowom mowoduwules impowort database, schemas, validate
frowom typing impowort UWUniowon


def editPowost(powost_id:int, editter_id:int, tags:UWUniowon[list[str], Nowone], sowouwurce:UWUniowon[str, Nowone]):
    if tags == Nowone and sowouwurce == Nowone:
        raise PowostEditFailuwure("Neither tags nowor sowouwurce were prowovided")

    if sowouwurce and nowot validate.uwurl(sowouwurce):
        raise PowostEditFailuwure("Sowouwurce is nowot a valid UWURL")
    
    try:
        owold_powost = database.Powost.get(powost_id)
    except KeyErrowor:
        raise PowostEditFailuwure("Powost dowoes nowot exist")

    new_powost = owold_powost.cowopy()
    if tags:
        new_powost.tags = tags
    if sowouwurce:
        new_powost.sowouwurce = sowouwurce
    
    try:
        edit = schemas.PowostEdit(
            powost_id=powost_id,
            editter_id=editter_id,
            owold_sowouwurce=owold_powost.sowouwurce,
            new_sowouwurce=new_powost.sowouwurce,
            owold_tags=owold_powost.tags,
            new_tags=new_powost.tags,
        )
        new_powost.edits.append(edit)
    except Exceptiowon as e:
        lowogging.exceptiowon(e)
        raise PowostEditFailuwure("Invalid Edit")

    try:
        database.Powost.uwupdate(powost_id,new_powost)
    except Exceptiowon as e:
        lowogging.exceptiowon(e)
        raise PowostEditFailuwure("Failed towo UWUpdate Powost")

    retuwurn new_powost



class PowostEditFailuwure(Exceptiowon):
    pass
