from openbooru.modules import settings
from openbooru.modules.schemas import Permission, UserPermissions
from typing_extensions import Self
import yaml as _yaml


with open("./settings.yml") as f:
    SETTING_LOOKUP = _yaml.full_load(f)['permissions']


class Permissions:
    schema:UserPermissions
    
    def __init__(self, permissions:UserPermissions):
        self.schema = permissions


    @classmethod
    def from_level(cls, level:str, lookup:dict = SETTING_LOOKUP) -> Self:
        """Raises:
        - KeyError: Invalid Level
        """
        if level not in lookup:
            raise KeyError(f"Level: {level} not defined in settings ")

        user_perms = {}
        actions:dict = lookup[level]
        for name, attributes in actions.items():
            user_perms[name] = construct_permission(attributes)

        permissions = UserPermissions.parse_obj(user_perms)
        return cls(permissions)


    def hasPermission(self, action:str) -> bool:
        permission = getattr(self.schema,action)
        return permission.has_permission


    def isCaptchaRequired(self, action:str) -> bool:
        permission = getattr(self.schema,action)
        return permission.captcha


    def getRateLimit(self, action:str) -> str|None:
        permission = getattr(self.schema,action)
        return permission.ratelimit


def construct_permission(attributes: dict|None) -> Permission:
    if attributes == None:
        permission = Permission()
    else:
        try:
            permission = Permission.parse_obj(attributes)
        except Exception:
            raise RuntimeError(f"Invalid Permission Specified in settings.yml\n{attributes}")

    if not settings.HCAPTCHA_ENABLED:
        permission.captcha = False
    
    permission.has_permission = True
    return permission
