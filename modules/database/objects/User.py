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
        {
            email      : n.email,
            settings   : n.settings,
            history    : COLLECT(viewed.id),
            favourites : COLLECT(favourited.id),
            blocked    : COLLECT(blocked.id)
        } as private
"""


def create(name:str,email:str):
    if not Validate.username(name):
        raise ValueError("Invalid Name for User Creation")
    if not Validate.email(email):
        raise ValueError("Invalid Email for User Creation")
    if not _isUnique.user_email(email):
        raise ValueError("Email already in use")
    if not _isUnique.user_name(name):
        raise ValueError("Name already in use")
    
    data = _db_run("""
        CREATE (n:User {
            created_at: TIMESTAMP(),
            name: $name,
            email: $email,
            level: "USER",
            description: "",
            settings: ""
        })
        RETURN ID(n)
    """,name=name,email=email)
    return data[0]['ID(n)']

def get(**kwargs) -> dict:
    """Get a user from it's unique kwarg value

    kwargs:
    - id
    - name
    
    Raises:
        KeyError: [description]
    """
    LOOKUP = {
        "id"   : [int,"WHERE ID(n) = $id"],
        "name" : [str,"WHERE n.name = $name"],
    }
    
    query = "MATCH (n:User)"
    query += _combine_kwargs(LOOKUP,kwargs) 
    query += _DATA_QUERY

    data = _db_run(query,**kwargs)
    if data:
        return data[0]
    else:
        raise KeyError('No User found with that ID/Name')

def search(limit:int=10,**kwargs) -> list[dict]:
    LOOKUP = {
        "created_at" : [int,"WHERE u.created_at = $created"],
        "name"       : [str,"WHERE u.name = $name"],
        "email"      : [str,"WHERE u.email = $email"],
        "level"      : [str,"WHERE u.level = $level"],
    }
    
    query = "MATCH (u:User)"
    query += _combine_kwargs(LOOKUP,kwargs) 
    query += _DATA_QUERY + "LIMIT $limit"
    return _db_run(query,limit=limit,**kwargs)

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

def view(id:int,post:int):
    ...

def toggle_favourite(id:int,post:int):
    ...

def toggle_block(id:int,post:int):
    ...

def toggle_upvote(id:int,post:int):
    ...

def toggle_downvote(id:int,post:int):
    ...
