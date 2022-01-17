from . import _combine_kwargs,_db_run
from dataclasses import dataclass
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
        creator.id as creator_id,
        ID(full) as full_id,
        ID(preview) as preview_id,
        ID(thumbnail) as thumbnail_id,
        
        n.created_at as created_at,
        n.type as type,
        n.sound as sound,
        n.source as source,
        n.rating as rating,
        full.md5 as md5,
        
        
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
"""

@dataclass(frozen=True)
class Post:
    id:int
    creator_id:int
    full_id:int
    preview_id:int
    thumbnail_id:int
    
    created_at:int
    type:str
    sound:bool
    source:str
    rating:str
    md5:str
    
    tags:str
    comments:list[int]
    annotations:list[dict]
    views:int
    upvotes:int
    downvotes:int
    score:int

def create(
        creator_id:int,full_id:int,preview_id:int,thumbnail_id:int,
        type:str,sound:bool,source:str,rating:str) -> Post:
    query = _CREATE_QUERY + _DATA_QUERY
    data = _db_run(query,
        creator=creator_id,prev=preview_id,full=full_id,thumb=thumbnail_id,
        src=source,rating=rating,type=type,sound=sound,
    )
    return Post(**data[0])


def get(id:int=None,md5:str=None) -> Post:
    """Get a post from a property

    Raises:
    - ValueError: No property specified
    - KeyError: No Post exists with that data
    """
    query = f"MATCH (n:Post)"
    kwargs = {}
    if id != None:
        query += "WHERE ID(n) = $id"
        kwargs |= {'id':id}
    if md5 != None:
        query += "MATCH (n)-[:Full]->(f:Image) WHERE f.md5 = $md5"
        kwargs |= {'md5':md5}
    
    if kwargs == {}:
        raise ValueError("No Properties Selected")
    data = _db_run(query + _DATA_QUERY,**kwargs)
    
    if data:
        return Post(**data[0])
    else:
        raise KeyError(f"No Post exists with that data")


def search(limit:int=32,order:str='created_at',
            tags:list[str]=None,sources:list[str]=None,
            types:list[str]=None,sound:bool=None,
            post_ids:list[int]=None,
            creator_names:list[str]=None,creator_ids:list[int]=None,
            before:int=None,after:int=None,
            views_less:int=None,views_more:int=None,
           ) -> list[Post]:
    """Search for posts

    Args:
        limit: The number of posts to return
        order: The order to sort the posts by. Valid Options:
            created_at: Sort by creation date
            id: The id of the post

    Raises:
        ValueError: Invalid Ordering
        ValueError: No Properties Selected
    """
    ORDERS = {'created_at':'n.created_at','id':'ID(n)'}
    if order not in ORDERS:
        raise ValueError("Invalid Ordering")
    
    query = "MATCH (n:Post)"
    kwargs = {}
    if tags != None:
        query += "MATCH (n)-[:Tagged]->(tag) WHERE tag.name IN $tags"
        kwargs |= {'tags':tags}
    if types != None:
        query += "WHERE n.type IN $types"
        kwargs |= {'types':types}
    if sound != None:
        query += "WHERE n.sound = $sound"
        kwargs |= {'sound':sound}
    if sources != None:
        query += "WHERE n.source IN $sources"
        kwargs |= {'sources':sources}
    
    if post_ids != None:
        query += "WHERE ID(n) IN $post_ids"
        kwargs |= {'post_ids':post_ids}
    
    if creator_names != None:
        query += "MATCH (n)-[:Created]->(u:User) WHERE u.name IN $creator_names"
        kwargs |= {'creator_names':creator_names}
    if creator_ids != None:
        query += "MATCH (n)-[:Created]->(u:User) WHERE ID(u) IN $creator_ids"
        kwargs |= {'creator_ids':creator_ids}
    
    if views_more != None:
        query += "WHERE n.views > $views_more"
        kwargs |= {'views_more':views_more}
    if views_less != None:
        query += "WHERE n.views < $views_less"
        kwargs |= {'views_kess':views_less}
    
    if after != None:
        query += "WHERE n.created_at > $after"
        kwargs |= {'after':after}
    if before != None:
        query += "WHERE n.created_at < $before"
        kwargs |= {'before':before}
    if kwargs == {}:
        raise ValueError("No Properties Selected")
    

    query += f"{_DATA_QUERY} ORDER BY {ORDERS[order]} LIMIT $limit"
    
    data = _db_run(query,limit=limit,**kwargs)
    return [Post(**a)for a in data]


def set(id:int,
        source:str=None,rating:str=None,
        annotations:list[dict]=None,tags:list[str]=None,
        ):
    """Set a Post Property
    """
    kwargs = {}
    if source is not None:
        kwargs |= {'source':source}
    if rating is not None:
        kwargs |= {'rating':rating}
    if annotations is not None:
        kwargs |= {'annotations':annotations}
    if tags is not None:
        kwargs |= {'tags':tags}
    LOOKUP = {
        'source'      : "SET p.source = $src",
        'rating'      : "SET p.rating = $rating",
        'annotations' : "SET p.annotations = $annotations",
        'tags'        : """
            MATCH (p)-[:Tagged]->(oldTag:Tag)
            CALL apoc.do.when(not oldTag.name in $tags,"
                MATCH (p)-[r:Tagged]->($tag)) DETACH DELETE r
            ","",{tag:oldTag}) YIELD value

            WITH COLLECT(oldTag.name) as oldTags
            UNWIND $tags as newTag
            CALL apoc.do.when(not newTag in oldTags,"
                MATCH (t:Tag {name:$tag}) CREATE (p)-[:Tagged]->(t)
            ","",{tag:newTag}) YIELD value
            RETURN null
        """,
    }
    
    query = "MATCH (p:Post) WHERE ID(p) = $id"
    query += _combine_kwargs(LOOKUP,kwargs)
    
    _db_run(query,id=id,**kwargs)


def delete(id:int):
    _db_run(
        "MATCH (n:Post) WHERE ID(n) = $id DETACH DELETE n",
        id=id
    )
