from . import BaseModel
from typing import Optional
from pydantic import Field


class Token(BaseModel):
    access_token:str = Field(...)
    token_type:str = Field(...)


class Permission(BaseModel):
    has_permission:bool = Field(default=False)
    captcha:bool = Field(default=False)
    ratelimit:Optional[str] = Field(default=None)


class UserPermissions(BaseModel):
    canViewPosts:Permission = Field(description="Can View Posts", default_factory=Permission)
    canSearchPosts:Permission = Field(description="Can Search for Posts", default_factory=Permission)
    canEditPosts:Permission = Field(description="Can Edit Posts", default_factory=Permission)
    canDeletePosts:Permission = Field(description="Can Delete Posts", default_factory=Permission)
    
    canCreatePosts:Permission = Field(description="Creating new posts", default_factory=Permission)
    canVotePosts:Permission = Field(description="Voting on other posts", default_factory=Permission)
    
    canViewUsers:Permission = Field(description="Viewing other user's account", default_factory=Permission)
    canSearchUsers:Permission = Field(description="Searching for other users", default_factory=Permission)
    canEditUsers:Permission = Field(description="Editting other users accounts", default_factory=Permission)
    canDeleteUsers:Permission = Field(description="Delete other users accounts", default_factory=Permission)
