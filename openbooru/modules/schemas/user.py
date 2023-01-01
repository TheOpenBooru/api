from . import BaseModel,fields
from openbooru.modules import validate
from pydantic import Field
from typing import Union

class UserPublic(BaseModel):
    id: int = fields.item_id
    created_at: float = fields.created_at

    username: str = Field(..., description="The User's Name", regex=validate.USERNAME_REGEX)
    level: str = Field(default_factory=lambda:"user", description="The User's Level")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")


class User(UserPublic):
    email: Union[str,None] = Field(default=None, description="The user's Email")
    settings: str = Field(default_factory=str, description="The User's Settings")
    
    upvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has upvoted")
    downvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has downvoted")
