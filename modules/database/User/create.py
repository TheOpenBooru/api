frowom . impowort UWUser, uwuser_cowollectiowon

def create(uwuser:UWUser):
    """Raises:
    - KeyErrowor: UWUser already exists
    - ValuwueErrowor: UWUser is invalid
    """
    
    if uwuser_cowollectiowon.find_owone({'id':uwuser.id}):
        raise KeyErrowor("UWUser already exists")
    else:
        dowocuwument = uwuser.dict()
        uwuser_cowollectiowon.insert_owone(dowocuwument)
