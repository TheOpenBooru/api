from . import _combine_kwargs,_db_run
from typing import Any

_DATA_QUERY = """
    MATCH (n)<-[:CreatedPost]-(creator:User)
    MATCH (n)-[:Full]->(full:Image)
    MATCH (n)-[:Preview]->(preview:Image)
    MATCH (n)-[:Thumbnail]->(thumbnail:Image)

    OPTIONAL MATCH (n) -[:Tagged]->(tag:Tag)
    OPTIONAL MATCH (n)<-[comment:Comment]-(:User)
    OPTIONAL MATCH (n)<-[view:View]-(:User)
    OPTIONAL MATCH (n)<-[annotation:Annotation]-(:User)
    OPTIONAL MATCH (n)<-[upvote:Upvote]-(:User)
    OPTIONAL MATCH (n)<-[downvote:Downvote]-(:User)
    RETURN
        ID(n) as id,
        n.created_at as created_at,
        n.type as type,
        n.sound as sound,
        n.source as source,
        n.rating as rating,
        full.md5 as md5,
        
        creator.id as creator_id,
        ID(full) as full_id,
        ID(preview) as preview_id,
        ID(thumbnail) as thumbnail_id,
        
        COLLECT(tag.type + ":" + tag.name) as tags,
        COLLECT(comment) as comments,
        COLLECT(annotation) as annotations,
        COUNT(view) as views,
        COUNT(upvote) as upvotes,
        COUNT(downvote) as downvotes,
        COUNT(upvote) - COUNT(downvote) as score
"""

_CREATE_QUERY = """
    MATCH (u:User) WHERE ID(u) = $creator
    MATCH (full:Image) WHERE ID(full) = $full
    MATCH (preview:Image) WHERE ID(preview) = $prev
    MATCH (thumbnail:Image) WHERE ID(thumbnail) = $thumb

    CREATE (p:Post {
        created_at:timestamp(),
        type:$type,
        sound:$sound,
        source:$src,
        rating:$rating
    })
    
    CREATE (p)<-[:CreatedPost]-(u)
    CREATE (p)-[:Full]->(full)
    CREATE (p)-[:Preview]->(preview)
    CREATE (p)-[:Thumbnail]->(thumbnail)

    RETURN ID(p)
"""

def create(
        creator_id:int,
        full_id:int,
        preview_id:int,
        thumbnail_id:int,
        type:str,
        sound:bool,
        source:str,
        rating:str) -> int:
    
    data = _db_run(_CREATE_QUERY,
        creator=creator_id,src=source,rating=rating,type=type,sound=sound,
        prev=preview_id,full=full_id,thumb=thumbnail_id,
    )
    return data[0]['ID(p)']


def get(**kwargs) -> dict:
    """Get a post from a unique kwarg
    
    kwargs:
    - id
    - md5

    Raises:
    - KeyError: No post with that criteria
    """
    LOOKUP = {
        "id"  : (int,"WHERE ID(n) = $id"),
        "md5" : (str,"MATCH (n)-[:Full]->(f:Image) WHERE f.md5 = $md5"),
        }
    
    query = "MATCH (n:Post) "
    query += _combine_kwargs(LOOKUP,kwargs)
    query += _DATA_QUERY
    data = _db_run(query,**kwargs)
    
    if data:
        return data[0]
    else:
        raise KeyError(f"No Post exists with that data, {kwargs=}")


def search(limit:int=32,order:str='created_at',**kwargs) -> list[dict[str,Any]]:
    ORDERS = {'created_at':'n.created_at','id':'ID(n)'}
    LOOKUP = {
        "tags"          : (list[str],"MATCH (n)-[:Tagged]->(tag) WHERE tag.name IN $tags"),
        "creator_names" : (list[str],"MATCH (n)-[:Created]->(u:User) WHERE u.name IN $creator_names"),
        "ids"           : (list[int],"WHERE ID(n) IN $ids"),
        "types"         : (list[str],"WHERE n.type = $types"),
        "sources"       : (list[str],"WHERE n.source IN $source"),
        "sound"         : (bool,"WHERE n.sound = $sound"),
        "after"         : (int,"WHERE n.created_at > $after"),
        "before"        : (int,"WHERE n.created_at < $before"),
        "views_more"    : (int,"WHERE n.views > $views_more"),
        "views_less"    : (int,"WHERE n.views < $views_less"),
        }
    
    if order not in ORDERS:
        raise ValueError("Invalid Ordering")

    query =  "MATCH (n:Post) ID(n)"
    query += _combine_kwargs(LOOKUP,kwargs)
    query += f"{_DATA_QUERY} ORDER BY {ORDERS[order]} LIMIT $limit"
    
    return _db_run(query,limit=limit,**kwargs)


def set(id:int,**kwargs):
    """Set a Post Property

    kwargs:
    - source(str)
    - rating(str)
    - annotations(list[dict])
    - tags(list[str])
    """
    LOOKUP = {
        'source'      : (str,"SET p.source = $src"),
        'rating'      : (str,"SET p.rating = $rating"),
        'annotations' : (list[dict],"SET p.annotations = $annotations"),
        'tags'        : (list[str],"""
            MATCH (p)-[:Tagged]->(oldTag:Tag)
            CALL apoc.do.when(not oldTag.name in $tags,"
                MATCH (p)-[r:Tagged]->($tag))
                DETACH DELETE r
            ","",{tag:oldTag}) YIELD value

            WITH COLLECT(oldTag.name) as oldTags
            UNWIND $tags as newTag
            CALL apoc.do.when(not newTag in oldTags,"
                MATCH (t:Tag {name:$tag})
                CREATE (p)-[:Tagged]->(t)
            ","",{tag:newTag}) YIELD value
            RETURN null
        """),
    }
    
    query = "MATCH (p:Post) WHERE ID(p) = $id"
    query += _combine_kwargs(LOOKUP,kwargs)
    
    _db_run(query,id=id,**kwargs)


def delete(id:int):
    _db_run(
        "MATCH (n:Post) WHERE ID(n) = $id DETACH DELETE n",
        id=id
    )
