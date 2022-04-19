from . import _user_store,get
import random

def get_unique_id() -> int:
    id = random.randint(0,2**32)
    while id in _user_store:
        id = random.randint(0,2**32)
    
    return id
