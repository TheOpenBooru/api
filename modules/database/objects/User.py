from ..types import User
import time
import random

_users:dict[int,User] = {}


def create(name:str,email:str) -> int:
    id = random.randint(0,2**64)
    _users[id] = User(
        id=id,created_at=int(time.time()),
        name=name,email=email,level="USER",
        description='',settings={},
        posts=[],comments=[],
        history=[],favourites=[],blocked=[],
        upvotes=[],downvotes=[],
        )
    return id


def get(id:int=None,name:str=None,email:str=None) -> User:
    """Raises:
        KeyError: No User with that ID
        ValueError: Invalid
    """
    if id:
        _filter = lambda x:x.id == id
    elif name:
        _filter = lambda x:x.name == name
    elif email:
        _filter = lambda x:x.email == email
    else:
        raise ValueError("No user specified")
    
    values = list(filter(_filter,list(_users.values())))
    assert len(values) == 1
    return values[0]


def search(limit:int=10,order:str='name',
           name_like:str=None,level:str=None,
           after:int=None,before:int=None,
           ) -> list[User]:
    """Valid Orders:
    - id
    - name
    - created_at
    """
    values = list(_users.values())
    if name_like:
        values = list(filter(lambda x:name_like in x.name,values))
    if level:
        values = list(filter(lambda x:x.level == level,values))
    if after:
        values = list(filter(lambda x:x.created_at > after,values))
    if before:
        values = list(filter(lambda x:x.created_at < before,values))
    values = sorted(values,key=lambda x:x.__getattribute__(order))
    return values


def set(id:int,
        name:str=None,email:str=None,
        level:str=None,description:str=None,
        settings:dict=None,
        ):
    user = _users[id]
    user.name = name or user.name
    user.email = email or user.email
    user.level = level or user.level
    user.description = description or user.description
    user.settings = settings or user.settings


def delete(id:int):
    _users.pop(id)


def view(id:int,post_id:int):
    _users[id].history.append(post_id)


def toggle_favourite(id:int,post_id:int):
    user = _users[id]
    if post_id in user.favourites:
        user.favourites.remove(post_id)
    else:
        user.favourites.append(post_id)


def toggle_block(id:int,post_id:int):
    user = _users[id]
    if post_id in user.blocked:
        user.blocked.remove(post_id)
    else:
        user.blocked.append(post_id)


def toggle_upvote(id:int,post_id:int):
    user = _users[id]
    if post_id in user.upvotes:
        user.upvotes.remove(post_id)
    else:
        user.upvotes.append(post_id)


def toggle_downvote(id:int,post_id:int):
    user = _users[id]
    if post_id in user.downvotes:
        user.downvotes.remove(post_id)
    else:
        user.downvotes.append(post_id)
