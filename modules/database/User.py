from modules.schemas import User

_users_store:dict[int,User] = {}




def create(user:User):
    _users_store[user.id] = user

def get_unused_id() -> int:
    return len(_users_store) + 1

def get(*,id:int=None,name:str=None) -> User | None:
    for user in _users_store.values():
        if ((id and user.id == id) or
            (name and user.name == name)):
            return user
    return None

def exists(id:int) -> bool:
    return id in _users_store

def search(limit:int=10,order:str='name',
           name:str=None,name_like:str=None,
           level:str=None
           ) -> list[User]:
    """Valid Orders:
    - name
    - created_at
    """
    def _filter(user:User):
        return (
            (name and name == user.name) or 
            (name_like and name_like in user.name) or 
            (level and level == user.level)
        )
    
    values = list(_users_store.values())
    values = list(filter(_filter,values))
    values.sort(key=lambda x:getattr(x,order))
    return values[:limit]


def set(id:int,user:User):
    _users_store[id] = user


def delete(id:int):
    _users_store.pop(id)

def clear():
    _users_store.clear()

def view(id:int,postID:int):
    _users_store[id].history.append(postID)


def toggle_favourite(id:int,postID:int):
    user = _users_store[id]
    if postID in user.favourites:
        user.favourites.remove(postID)
    else:
        user.favourites.append(postID)


def toggle_block(id:int,postID:int):
    user = _users_store[id]
    if postID in user.blocked:
        user.blocked.remove(postID)
    else:
        user.blocked.append(postID)


def toggle_upvote(id:int,postID:int):
    user = _users_store[id]
    if postID in user.upvotes:
        user.upvotes.remove(postID)
    else:
        user.upvotes.append(postID)


def toggle_downvote(id:int,postID:int):
    user = _users_store[id]
    if postID in user.downvotes:
        user.downvotes.remove(postID)
    else:
        user.downvotes.append(postID)
