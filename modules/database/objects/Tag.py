from ..types import Tag
import time

_tags = dict()

def _create_default_tag(name:str):
    tag = Tag(
        created_at=int(time.time()),count=0,
        name=name,namespace='generic',
        )
    _tags[name] = tag

def get(name:str) -> Tag:
    if name not in _tags:
        _create_default_tag(name)
    return _tags[name]

def search(limit:int=32,order:str='count',
           namespace:str=None,
           before:int=None,after:int=None,
           ) -> list[Tag]:
    """Raises:
        ValueError: Invalid order
    """
    ORDERS = {
        'count':lambda x:x.count,
        'name':lambda x:x.name,
    }
    
    def _filter(tag:Tag):
        return not (
            (namespace and tag.namespace != namespace) or
            (before and tag.created_at > before) or 
            (after and tag.created_at < after)
            )
    
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