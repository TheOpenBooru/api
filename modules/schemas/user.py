from pydantic import BaseModel, Field,AnyHttpUrl,FileUrl
from typing import Optional
from time import time
from . import fields

class User_Public(BaseModel):
    id: int = Field(..., description="The User's ID")
    created_at: float = Field(default_factory=time, description="Unix timestamp for when the User was created")

    name: str = Field(..., description="The User's Name")
    level: str = Field(default_factory=lambda:"USER", description="The User's Level")
    posts: list[int] = Field(default_factory=list, description="IDs of Posts made by the user")
    comments: list[int] = Field(default_factory=list, description="IDs of Comments made by the user")

class User(User_Public):
    email: str = Field(..., description="The User's Email Address")
    settings: str = Field(default_factory=str, description="The User's Settings")
    
    upvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has upvoted")
    downvotes: list[int] = Field(default_factory=list, description="IDs of posts the user has downvoted")
    history: list[int] = Field(default_factory=list, description="IDs of recently viewed posts")

