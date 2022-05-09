from . import BaseModel,fields
from pydantic import Field
from time import time

class User_Query(BaseModel):
    username:str|None = Field(default=None)
    email:str|None = Field(default=None)


class User_Public(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At

    username: str = Field(..., description="The User's Name")
    level: str = Field(default_factory=lambda:"user", description="The User's Level")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")


class User(BaseModel):
    id: int = fields.Item_ID
    created_at: float = fields.Created_At

    username: str = Field(..., description="The User's Name")
    level: str = Field(default_factory=lambda:"user", description="The User's Level")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")
    
    email: str|None = Field(default=None, description="The User's Email Address")
    settings: dict = Field(default_factory=dict, description="The User's Settings")
    
    upvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has upvoted")
    downvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has downvoted")
    history: list[int] = Field(default_factory=list, description="IDs of recently viewed posts")
