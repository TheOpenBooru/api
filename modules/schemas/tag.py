from . import fields, BaseModel
from modules import validate
from pydantic import Field
from typing import Union

class Tag(BaseModel):
    name: str = Field(...,description="The Tag Name", regex=validate.TAG_REGEX)
    created_at:float = fields.Created_At
    namespace: str = Field(default="generic", description="The Tag Namespace")
    count: int = Field(default=0, description="The number of times the tag has been used")

class Tag_Query(BaseModel):
    name_like: Union[str,None] = Field(default=None, description="Tags with a section of the tag name, does not guarantee all results")
    namespace: Union[str,None] = Field(default=None, description="The namespace of the tags")
    count_gt: Union[str,None] = Field(default=None, description="Tags with a count greater than this")
    limit: int = Field(default=20, lt=101, description="The number of results to return")
