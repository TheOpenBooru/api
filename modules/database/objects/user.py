from dataclasses import dataclass

from modules.database.objects import user
from . import _db_run,_combine_kwargs,_isUnique,Validate

_DATA_QUERY = """
    OPTIONAL MATCH (n)-[:Created]->(post:Post)
    OPTIONAL MATCH (n)-[:Created]->(comment:Comment)
    OPTIONAL MATCH (n)-[:Viewed]->(viewed:Post)
    OPTIONAL MATCH (n)-[:Favourited]->(favourited:Post)
    OPTIONAL MATCH (n)-[:Blocked]->(blocked:Post)
    RETURN
        ID(n) as id,
        n.created_at as created_at,
        n.level as level,
        n.name as name,
        n.description as description,
        COLLECT(post.id) as posts,
        COLLECT(comment.id) as comments,
        
        p_email as n.email,
        p_settings as n.settings,
        p_history as COLLECT(viewed.id),
        p_favourites as COLLECT(favourited.id),
        p_blocked as COLLECT(blocked.id)
"""

@dataclass(frozen=True)
class User:
        id:int
        created_at:int
        level:str
        name:str
        description:str
        posts:list[int]
        comments:list[int]
        
        p_email:str
        p_settings:dict
        p_history:list[int]
        p_favourites:list[int]
        p_blocked:list[int]


def create(name:str,email:str) -> User:
    """Create a new user
    
    Raises:
        ValueError: Invalid Name or Email
        ValueError: Name or Email Already in Use
    """
    if not Validate.username(name):
        raise ValueError("Invalid Name")
    if not Validate.email(email):
        raise ValueError("Invalid Email")
    if not _isUnique.user_email(email):
        raise ValueError("Email Already in Use")
    if not _isUnique.user_name(name):
        raise ValueError("Name Already in Use")
    query = """
        CREATE (n:User {
            created_at: TIMESTAMP(),
            name: $name,
            email: $email,
            level: "USER",
            description: "",
            settings: ""
        })
    """
    query += _DATA_QUERY
    data = _db_run(query,name=name,email=email)
    return User(**data[0])


def get(id:int=None,name:str=None,email:str=None) -> User:
    """Get a user from it's unique kwarg value
    
    Raises:
        KeyError: No User found with that Identifier
    """
    query = "MATCH (n:User) "
    kwargs = {}
    if id is not None:
        query += " WHERE ID(n) = $id"
        kwargs |= {"id":id}
    if name is not None:
        query += " WHERE n.name = $name"
        kwargs |= {"name":name}
    if email is not None:
        query += " WHERE n.email = $email"
        kwargs |= {"email":email}

    query += _DATA_QUERY
    data = _db_run(query,**kwargs)
    if data:
        return User(**data[0])
    else:
        raise KeyError('No User found with that Identifier')


def search(limit:int=10,**kwargs) -> list[User]:
    LOOKUP = {
        "created_at" : [int,"WHERE u.created_at = $created"],
        "name"       : [str,"WHERE u.name = $name"],
        "email"      : [str,"WHERE u.email = $email"],
        "level"      : [str,"WHERE u.level = $level"],
    }
    
    query = "MATCH (u:User)"
    query += _combine_kwargs(LOOKUP,kwargs) 
    query += _DATA_QUERY + "LIMIT $limit"
    data = _db_run(query,limit=limit,**kwargs)
    return [User(**x) for x in data]


def set(id:int,**kwargs):
    LOOKUP = {
        "level"     : [str,"SET n.level = $level"],
        "name"      : [str,"SET n.name = $name"],
        "email"     : [str,"SET n.email = $email"],
        "description":[str,"SET n.description = $description"],
        "settings"  : [str,"SET n.settings = $settings"],
    }
    
    query = "MATCH (u:User) WHERE ID(u) = $id"
    query += _combine_kwargs(LOOKUP,kwargs)
    _db_run(query,id=id,**kwargs)


def delete(id:int):
    _db_run(
        "MATCH (n:User) WHERE ID(n) = $id DELETE n",
        id=id
    )


def view(id:int,post_id:int):
    raise NotImplementedError


def toggle_favourite(id:int,post_id:int):
    raise NotImplementedError


def toggle_block(id:int,post_id:int):
    raise NotImplementedError


def toggle_upvote(id:int,post_id:int):
    raise NotImplementedError

def toggle_downvote(id:int,post_id:int):
    raise NotImplementedError
