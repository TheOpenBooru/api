from typing import Union
from typing_extensions import Self, ClassVar
from modules.schemas import Permission, UserPermissions
import yaml as _yaml


with open("./settings.yml") as f:
    SETTING_LOOKUP = _yaml.full_load(f)['permissions']


class Permissions:
    permissions:UserPermissions
    
    def __init__(self, permissions:UserPermissions):
        self.permissions = permissions


    @classmethod
    def from_level(cls, level:str, lookup:dict = SETTING_LOOKUP) -> Self:
        """Raises:
        - KeyError: Invalid Level
        """
        if level not in lookup:
            raise KeyError("Invalid Level")

        user_perms = {}
        actions:dict = lookup[level]
        for name, attributes in actions.items():
            user_perms[name] = construct_permission(attributes)

        permissions = UserPermissions.parse_obj(user_perms)
        return cls(permissions)


    def hasPermission(self, action:str) -> bool:
        permission = getattr(self.permissions,action)
        return permission.has_permission


    def isCaptchaRequired(self, action:str) -> bool:
        permission = getattr(self.permissions,action)
        return permission.captcha


    def getRateLimit(self, action:str) -> str:
        permission = getattr(self.permissions,action)
        return permission.ratelimit


def construct_permission(attributes:Union[dict,None]) -> Permission:
    if attributes == None:
        permission = Permission()
    else:
        permission = Permission.parse_obj(attributes)
    permission.has_permission = True
    return permission
