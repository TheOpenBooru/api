from pydantic import BaseModel as _PydanticBaseModel
class BaseModel(_PydanticBaseModel):
    class Config:
        smart_union = True


from . import fields
from .media import GenericMedia, Animation, Video, Image
from .misc import Author, Comment
from .tag import Tag, Tag_Query
from .post import Post, PostEdit, Post_Query, Valid_Post_Ratings, Valid_Post_Sorts, Hashes
from .user import User, User_Public