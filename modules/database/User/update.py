import json
from . import user_collection

def updateSettings(user_id:int, settings:str):
    """Raises:
    - ValueError: Settings must be less than 4096 characters
    """
    if len(settings) > 4096:
        raise ValueError("Settings must be less than 4096 characters")
    user_collection.update_one(
        filter={'id':user_id},
        update={'$set':{'settings':settings}}
    )
