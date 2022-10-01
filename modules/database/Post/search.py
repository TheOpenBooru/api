from . import Post, post_collection, parse_docs
from .. import Tag
from modules import schemas, settings
from pymongo import DESCENDING, ASCENDING


DEFAULT_QUERY = schemas.PostQuery()
def search(query:schemas.PostQuery = DEFAULT_QUERY) -> list[Post]:
    "Warning: Not-always consistent, implements caching"
    pipeline = []
    if settings.POSTS_SEARCH_USE_SIBLINGS_AND_PARENTS:
        pipeline.extend(APPEND_TAG_SIBLINGS_AND_PARENTS)
    pipeline.extend(build_pipeline(query))
    pipeline.append({"$sort":{
        query.sort: DESCENDING if query.descending else ASCENDING
    }})
    pipeline.append({"$skip": query.index})
    pipeline.append({"$limit": query.limit})
    cursor = post_collection.aggregate(pipeline=pipeline)
    return parse_docs(cursor)


def build_pipeline(query:schemas.PostQuery) -> list[dict]:
    filters = []
    
    if query.media_types:
        filters.append({'media_type':{'$in': query.media_types}})
    if query.ratings:
        filters.append({'rating':{'$in': query.ratings}})

    if query.include_tags and query.include_tags != []:
        filters.append({"tags":{'$all': query.include_tags}})
    if query.exclude_tags and query.exclude_tags != []:
        filters.append({"tags":{'$not': {'$all': query.exclude_tags}}})
    
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
        ]})
    
    return [{"$match": filter} for filter in filters]


APPEND_TAG_SIBLINGS_AND_PARENTS = [
    {
        '$lookup': {
            'from': 'tags', 
            'localField': 'tags', 
            'foreignField': 'name', 
            'as': 'tag_objects'
        }
    }, {
        '$lookup': {
            'from': 'tags', 
            'localField': 'tags', 
            'foreignField': 'siblings', 
            'as': 'sibling_objects'
        }
    }, {
        '$set': {
            'search_tags': {
                '$setUnion': [
                    '$tags',
                    '$tag_objects.name',
                    '$tag_objects.siblings',
                    '$tag_objects.parents',
                    '$sibling_objects.name',
                    '$sibling_objects.siblings',
                    '$sibling_objects.parents'
                ]
            }
        }
    }, {
        '$unset': [
            'tag_objects', 'sibling_objects'
        ]
    }, {
        '$unwind': {
            'path': '$tags', 
            'preserveNullAndEmptyArrays': True
        }
    }, {
        '$unwind': {
            'path': '$tags', 
            'preserveNullAndEmptyArrays': True
        }
    }, {
        '$group': {
            '_id': '$_id', 
            'tags': {
                '$push': '$tags'
            }, 
            'doc': {
                '$first': '$$ROOT'
            }
        }
    }, {
        '$replaceRoot': {
            'newRoot': {
                '$mergeObjects': [
                    '$doc', {
                        'tags': '$tags'
                    }
                ]
            }
        }
    }
]