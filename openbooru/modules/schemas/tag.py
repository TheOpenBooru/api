from . import fields, BaseModel, MAX_NUMBER
from openbooru.modules import validate
from pydantic import Field
from typing import Union


class Tag(BaseModel):
    name: str = Field(...,description="The Tag Name", regex=validate.TAG_REGEX)
    created_at:float = fields.created_at
    namespace: str = Field(default="generic", description="The Tag Namespace")
    count: int = Field(default=0, description="The number of times the tag has been used")
    siblings: list[str] = Field(default_factory=list, description="All the tag siblings for this tag")
    parents: list[str] = Field(default_factory=list, description="All the tag parents of this tag")


class TagQuery(BaseModel):
    name_like: Union[str,None] = Field(default=None, description="Tags with a section of the tag name, does not guarantee all results")
    namespace: Union[str,None] = Field(default=None, description="The namespace of the tags")
    count_lt: Union[int,None] = Field(default=None, ge=0, lt=MAX_NUMBER, description="Tags with a count less than this")
    count_gt: Union[int,None] = Field(default=None, ge=0, lt=MAX_NUMBER, description="Tags with a count greater than this")
    limit: int = Field(default=10, lt=51, description="The number of results to return")
