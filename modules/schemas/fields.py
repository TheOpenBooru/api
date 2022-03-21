from pydantic import Field as _Field
from modules import validate as _validate
import time as _time

Created_At:float = _Field(
    default_factory=_time.time,
    description="The Unix timestamp for when the Post was created",
)
Email:str = _Field(
    ...,
    description="The Unix timestamp for when the Post was created",
)
Lanugage = _Field(
    default=None,
    description="ISO 639-2 language code",
    regex="^[a-z]{3}$",
)
Age_Rating = _Field(
    default=None,
    description="Age rating of the post",
    regex="^(safe|questionable|explicit)$",
)
Source = _Field(
    default=None,
    description="Source URL of the image",
)
Tags:list[str] = _Field(
    default_factory=list,
    description="Tags on the post",
    unique_items=True,
    regex=_validate.TAG_REGEX
)
Comments = _Field(
    default_factory=list,
    description="Comments on the post",
)
Post_Type:str = _Field(
    ..., # Required
    description="Format of the post",
    regex="^(image|gif|video)$",
)
Mimetype:str = _Field(
    ...,
    description="The MIME type for the File",
    regex="^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+$",
)
Full_Image = _Field(
    ..., # Required
    description="The full scale media for the Post",
)
Preview_Image = _Field(
    default=None,
    description="A Medium Scale Version for the image, for hi-res posts",
)
Thumbnail_Image = _Field(
    ..., # Required,
    description="The lowest scale version of the image, for thumbnails",
)
Item_ID = _Field(
    ...,
    description="The Unique ID for this Item",
)
User_ID:int = _Field(
    ...,
    description="The User ID of the Post Creator"
)