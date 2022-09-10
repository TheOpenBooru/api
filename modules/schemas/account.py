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
    canLogin:Permission = Field(description="Logging in and Generating a Token", default_factory=Permission)
    canRegister:Permission = Field(description="Registering an Account", default_factory=Permission)
    
    canViewPosts:Permission = Field(description="Viewing Indiivudal Posts", default_factory=Permission)
    canSearchPosts:Permission = Field(description="Searching for Posts", default_factory=Permission)
    canEditPosts:Permission = Field(description="Editting Posts", default_factory=Permission)
    canDeletePosts:Permission = Field(description="Deleting Posts", default_factory=Permission)
    
    canRecieveAllTags:Permission = Field(description="Getting a list of every tag", default_factory=Permission)
    canSearchTags:Permission = Field(description="Can search for tags", default_factory=Permission)
    
    canViewUsers:Permission = Field(description="Viewing other user's account", default_factory=Permission)
    canSearchUsers:Permission = Field(description="Searching for other users", default_factory=Permission)
    canEditUsers:Permission = Field(description="Editting other users accounts", default_factory=Permission)
    canDeleteUsers:Permission = Field(description="Delete other users accounts", default_factory=Permission)
    canCreatePosts:Permission = Field(description="Creating new posts", default_factory=Permission)
    canVotePosts:Permission = Field(description="Voting on other posts", default_factory=Permission)
    
    canViewProfile:Permission = Field(description="Viewing Own Profile", default_factory=Permission)
    canUpdateSettings:Permission = Field(description="Updaing Profile Settings", default_factory=Permission)
