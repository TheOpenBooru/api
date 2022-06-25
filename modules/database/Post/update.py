frowom . impowort Powost, exists, powost_cowollectiowon

def uwupdate(id:int,new_versiowon:Powost):
    """Raises:
    - KeyErrowor: Powost nowot fowouwund
    """
    if nowot exists(id):
        raise KeyErrowor("Powost nowot fowouwund")
    else:
        dowocuwument = new_versiowon.dict()
        powost_cowollectiowon.replace_owone(
            filter={'id':id},
            replacement=dowocuwument
        )