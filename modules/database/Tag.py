from modules.schemas import Tag
import time

_tags = dict()

def create(tag:Tag):
    _tags[tag.name] = tag

def get(name:str) -> Tag:
    return _tags[name]

def search(limit:int=32,order:str='count',
           namespace:str=None,
           after:int=None,before:int=None,
           ) -> list[Tag]:
    """Raises:
        ValueError: Invalid order
    """
    ORDERS = {
        'count':lambda x:x.count,
        'name':lambda x:x.name,
    }
    
    def _filter(tag:Tag):
        if namespace and tag.namespace != namespace:
            return False
        if before and tag.created_at > before:
            return False
        if after and tag.created_at < after:
            return False
        return True
    
    returnTags = list(filter(_filter,list(_tags.values())))
    returnTags.sort(key=ORDERS[order])
    return returnTags[:limit]


def set(name:str,namespace:str=None):
    tag = get(name)
    tag.namespace = namespace or tag.namespace


def list_all() -> list[Tag]:
    return list(_tags.values())


def delete(name:str):
    _tags.pop(name)