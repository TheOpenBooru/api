from . import BaseModel,fields
from pydantic import Field
from typing import Union

class User_Public(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At

    username: str = Field(..., description="The User's Name")
    level: str = Field(default_factory=lambda:"user", description="The User's Level")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")


class User(BaseModel):
    id: int = Field(..., description="The user's unique ID")
    created_at: float = fields.Created_At

    username: str = Field(..., description="The User's Name")
    level: str = Field(default_factory=lambda:"user", description="The User's Level")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")
    
    email: Union[str,None] = Field(default=None, description="The User's Email Address")
    settings: str = Field(default_factory=str, description="The User's Settings")
    
    upvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has upvoted")
    downvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has downvoted")
