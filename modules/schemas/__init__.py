from pydantic import BaseModel as _PydanticBaseModel
class BaseModel(_PydanticBaseModel):
    class Config:
        smart_union = True


from . import fields
from .media import GenericMedia, Animation, Video, Image
from .misc import Author, Comment, Status
from .tag import Tag, Tag_Query
from .post import Post, Post_Edit, Post_Query, Ratings, Sort, Hashes, Media_Type
from .user import User, User_Public