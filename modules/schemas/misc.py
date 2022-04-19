from . import Image,fields,BaseModel
from pydantic import Field


class Status(BaseModel):
    version: str = Field(..., description="The current API version")
    status: bool = Field(..., description="Is the server up?")


class Author(BaseModel):
    id: int = fields.Item_ID
    created_at:float = fields.Created_At
    name: str = Field(..., description="The Author's Name")
    avatar: Image = Field(..., description="The Author's Avatar")
    aliases: list[str] = Field(default_factory=list, description="Other Names for the Author")
    user_account: int = Field(..., description="The ID of the Account Bound to the Author")


class Tag(BaseModel):
    id: int = fields.Item_ID
    created_at:float = fields.Created_At
    name: str = Field(...,description="The Tag Name")
    namespace: str = Field(..., description="The Tag Namespace")
    count: int = Field(default_factory=int, description="The number of times the tag has been used")


class Comment(BaseModel):
    id: int = fields.Item_ID
    created_at:float = fields.Created_At
    creator: int = Field(..., description="The User ID of the Comment Creator")
    text: str = Field(..., description="The Comment's text")
    post: int = Field(..., description="The Post ID the Comment is on")
