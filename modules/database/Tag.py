from collections import defaultdict
from modules.schemas import Tag
from . import Post
import time

_tag_store = {}

def get(name:str) -> Tag:
    if name in _tag_store:
        return _tag_store[name]
    else:
        tag = Tag(name=name,namespace='generic')
        _tag_store[name] = tag
        return tag

def update(name:str,namespace:str|None=None):
    tag = get(name)
    tag.namespace = namespace or tag.namespace

def all() -> list[Tag]:
    tag_counts = {}
    for post in Post.all():
        for tag in post.tags:
            count = tag_counts.get(tag,0)
            tag_counts[tag] = count + 1
    all_tags = [get(x) for x in tag_counts]
    return all_tags
