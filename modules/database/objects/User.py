from ..types import User
import time
import random

_users_store:dict[int,User] = {}


def create(name:str,email:str) -> User:
    id = len(_users_store) + 1
    user = User(
        id=id,created_at=int(time.time()),
        name=name,email=email,
        level="USER",
        )
    _users_store[id] = user
    return user


def get(*,id:int=None,name:str=None) -> User | None:
    for user in _users_store.values():
        if ((id and user.id == id) or
            (name and user.name == name)):
            return user
    return None

def exists(id:int) -> bool:
    return id in _users_store

def search(limit:int=10,order:str='name',
           name_like:str=None,level:str=None,
           after:int=None,before:int=None,
           name:str=None,email:str=None,
           ) -> list[User]:
    """Valid Orders:
    - name
    - created_at
    """
    values = list(_users_store.values())
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
        settings:str=None,
        ):
    user = _users_store[id]
    user.name = name or user.name
    user.email = email or user.email
    user.level = level or user.level
    user.bio = description or ""
    user.settings = settings or ""


def delete(id:int):
    _users_store.pop(id)


def view(id:int,post_id:int):
    _users_store[id].history.append(post_id)


def toggle_favourite(id:int,post_id:int):
    user = _users_store[id]
    if post_id in user.favourites:
        user.favourites.remove(post_id)
    else:
        user.favourites.append(post_id)


def toggle_block(id:int,post_id:int):
    user = _users_store[id]
    if post_id in user.blocked:
        user.blocked.remove(post_id)
    else:
        user.blocked.append(post_id)


def toggle_upvote(id:int,post_id:int):
    user = _users_store[id]
    if post_id in user.upvotes:
        user.upvotes.remove(post_id)
    else:
        user.upvotes.append(post_id)


def toggle_downvote(id:int,post_id:int):
    user = _users_store[id]
    if post_id in user.downvotes:
        user.downvotes.remove(post_id)
    else:
        user.downvotes.append(post_id)
