import yaml
from pydantic import BaseModel

with open("./data/permissions.yml") as f:
    _permission_lookup = yaml.full_load(f)

class Permissions(BaseModel):
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


def permissions_from_level(level:str) -> Permissions:
    """Raises:
    - KeyError: Invalid Level
    """
    level = level.lower()
    if level not in _permission_lookup:
        raise KeyError("Invalid Level")
    else:
        valid_actions = _permission_lookup[level]
        object_form = {action:True for action in valid_actions}
        return Permissions.parse_obj(object_form)
