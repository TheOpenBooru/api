from xml.etree.ElementInclude import include
from . import Post, post_collection
from modules import schemas
import pymongo

def search(query:schemas.Post_Query) -> list[Post]:
    filters = []
    if query.include_tags:
        filters.append({'tags':{'$all':query.include_tags}})
    if query.exclude_tags:
        filters.append({'tags':{'$nin':query.exclude_tags}})
    if query.md5:
        filters.append({'md5s':{'$elemMatch':{"$eq":query.md5}}})
    if query.sha256:
        filters.append({'sha256s':{'$elemMatch':{"$eq":query.sha256}}})
    if query.created_after:
        filters.append({'created_at':{"$gt":query.created_after}})
    if query.created_before:
        filters.append({'created_at':{"$lt":query.created_before}})

    direction = pymongo.DESCENDING if query.descending else pymongo.ASCENDING
    cursor = post_collection.find(
        filter={'$and':filters} if filters else {},
        skip=query.index,
        limit=query.limit,
        sort=[(query.sort,direction)],
    )
    return [Post.parse_obj(doc) for doc in cursor]
