from pydantic import BaseModel as _PydanticBaseModel
class BaseModel(_PydanticBaseModel):
    class Config:
        smart_union = True
        json_encoders = { bytes: lambda _bytes: _bytes.hex() }

MAX_NUMBER = 2**63

from . import fields
from .subscription import Subscription, SubscriptionQuery
from .media import GenericMedia, Animation, Video, Image, MediaType
from .account import Permission, UserPermissions, Token
from .misc import Author, Comment, Status
from .tag import Tag, TagQuery
from .post import Post, PostEdit, PostQuery, Rating, Sort, Hashes
from .user import User, UserPublic