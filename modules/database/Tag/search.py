from . import Tag, tag_collection
from modules import schemas
import re

def search(query:schemas.Tag_Query) -> list[Tag]:
    filters = []
    if query.name_like:
        filters.append({'name':re.compile(query.name_like)})
    if query.namespace:
        filters.append({'namespace':query.namespace})
    if query.count_lt:
        filters.append({'count':{"$lt":query.count_lt}})
    if query.count_gt:
        filters.append({'count':{"$gt":query.count_gt}})

    kwargs = {}
    if query.limit:
        kwargs['limit'] = query.limit
    cursor = tag_collection.find(
        filter={'$and':filters} if filters else {},
        sort=[("count",-1)],
        **kwargs
    )
    return [Tag.parse_obj(doc) for doc in cursor]