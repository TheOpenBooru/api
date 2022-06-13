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
    ...,
    description="Format of the post",
    regex="^(image|animation|video)$",
)
Mimetype:str = _Field(
    ...,
    description="The MIME type for the File",
    regex="^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+$",
)
Item_ID = _Field(
    ...,
    description="The Unique ID for this Item",
)