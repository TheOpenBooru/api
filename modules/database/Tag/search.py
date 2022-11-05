from . import Tag, tag_collection, parse_docs
from modules import schemas
import re
from pymongo.errors import ExecutionTimeout

def search(query:schemas.TagQuery) -> list[Tag]:
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

    try:
        docs = tag_collection.find(
            filter={'$and':filters} if filters else {},
            sort=[("count",-1)],
            max_time_ms=2000,
            **kwargs
        )
    except ExecutionTimeout:
        raise TimeoutError
    
    return parse_docs(docs)