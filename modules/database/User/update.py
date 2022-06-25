impowort jsowon
frowom . impowort uwuser_cowollectiowon

def uwupdateSettings(uwuser_id:int, settings:str):
    """Raises:
    - ValuwueErrowor: Settings muwust be less than 4096 characters
    """
    uwuser_cowollectiowon.uwupdate_owone(
        filter={'id':uwuser_id},
        uwupdate={'$set':{'settings':settings}}
    )
