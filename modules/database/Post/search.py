from . import Post, post_collection, parse_docs
from .. import Tag
from modules import schemas
import pymongo


DEFAULT_QUERY = schemas.PostQuery()
def search(query:schemas.PostQuery = DEFAULT_QUERY) -> list[Post]:
    "Warning: Not-always consistent, implements caching"
    direction = pymongo.DESCENDING if query.descending else pymongo.ASCENDING
    cursor = post_collection.find(
        filter=build_filter(query),
        skip=query.index,
        limit=query.limit,
        sort=[(query.sort,direction)],
    )
    return parse_docs(cursor)


def build_filter(query:schemas.PostQuery) -> dict:
    filters = []
    
    if query.media_types:
        filters.append({'media_type':{'$in': query.media_types}})
    if query.ratings:
        filters.append({'rating':{'$in': query.ratings}})
    
    if query.include_tags:
        include_groups = construct_tag_groups(query.include_tags)
        filters.append({'$and':[
            {"tags": {"$in": group}}
            for group in include_groups
        ]})
    if query.exclude_tags:
        exclude_groups = construct_tag_groups(query.exclude_tags)
        filters.append({'$and':[
            {"tags": {"$nin": group}}
            for group in exclude_groups
        ]})
    
    if query.upvotes_gt:
        filters.append({"upvotes":{"$gt": query.upvotes_gt}})
    if query.upvotes_lt:
        filters.append({"upvotes":{"$lt": query.upvotes_lt}})
    
    if query.created_after:
        filters.append({'created_at':{"$gt": query.created_after}})
    if query.created_before:
        filters.append({'created_at':{"$lt": query.created_before}})
    
    if query.ids:
        filters.append({"id":{'$in': query.ids}})
    if query.md5:
        filters.append({"hashes":{'md5s':{'$elemMatch':{"$eq":query.md5}}}})
    if query.sha256:
        filters.append({"hashes":{'sha256s':{'$elemMatch':{"$eq":query.sha256}}}})
    if query.source:
        filters.append({"$or": [
            {"source": query.source},
            {"source": {'$elemMatch':{"$eq": query.source}}},
            ]
        })

    if filters:
        return {'$and':filters}
    else:
        return {}


def construct_tag_groups(tags:list[str]) -> list[list[str]]:
    sibling_groups = construct_sibling_groups(tags)
    parent_groups = construct_parent_groups(tags)
    
    tag_groups = [a + b for a,b in zip(sibling_groups, parent_groups)]
    tag_groups = [list(set(x)) for x in tag_groups]
    
    return tag_groups


def construct_sibling_groups(tags:list[str]) -> list[list[str]]:
    docs = Tag.tag_collection.find(
        filter={"siblings": {"$in": tags}}
    )
    sibling_groups = []
    for tag in tags:
        group = []
        group.append(tag)
        for doc in docs:
            if tag in doc["siblings"]:
                group.append(doc["name"])
                group.extend(doc["siblings"])
        sibling_groups.append(group)
    
    return sibling_groups


def construct_parent_groups(tags:list[str]) -> list[list[str]]:
    docs = Tag.tag_collection.find(
        filter={"parents": {"$elemMatch": {"$in": tags}}}
    )
    
    parent_groups = []
    for tag in tags:
        group = []
        group.append(tag)
        for doc in docs:
            if tag in doc["parents"]:
                group.append(doc["name"])
        parent_groups.append(group)

    
    return parent_groups
