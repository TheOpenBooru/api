from . import user_collection
import random

def get_unique_id() -> int:
    id = random.randint(0,2**32)
    while user_collection.find_one({'id':id}):
        id = random.randint(0,2**32)
    return id
