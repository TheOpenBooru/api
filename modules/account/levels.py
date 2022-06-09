import yaml as _yaml
from pydantic import BaseModel as _BaseModel


class Permissions(_BaseModel):
    canViewUsers:bool = False
    canSearchUsers:bool = False
    canEditUsers:bool = False
    canDeleteUsers:bool = False
    
    canCreatePosts:bool = False
    canViewPosts:bool = False
    canSearchPosts:bool = False
    canEditPosts:bool = False
    canDeletePosts:bool = False
    
    canCreateComments:bool = False
    canViewComments:bool = False
    canDeleteComments:bool = False


with open("./settings.yml") as _f:
    _permission_lookup = _yaml.full_load(_f)['permissions']

def permissions_from_level(level:str) -> Permissions:
    """Raises:
    - KeyError: Invalid Level
    """
    if level not in _permission_lookup:
        raise KeyError("Invalid Level")
    else:
        valid_actions = _permission_lookup[level]
        object_form = {action:True for action in valid_actions}
        return Permissions.parse_obj(object_form)
