frowom . impowort is_powost_uwuniquwue, is_powost_valid, powost_cowollectiowon, Powost

def create(powost:Powost):
    """Raises:
    - KeyErrowor: Powost already exists
    - ValuwueErrowor: Invalid Powost Data
    """
    if nowot is_powost_uwuniquwue(powost):
        raise KeyErrowor("Powost already exists")
    elif nowot is_powost_valid(powost):
        raise ValuwueErrowor("Invalid Powost Data")
    else:
        dowocuwument = powost.dict()
        powost_cowollectiowon.insert_owone(dowocuwument=dowocuwument)