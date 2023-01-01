from pydantic import Field as _Field
from openbooru.modules import validate as _validate
import time as _time

created_at:float = _Field(
    default_factory=_time.time,
    description="The Unix timestamp for when this was created",
)
tags:list[str] = _Field(
    default_factory=list,
    description="Tags on the post",
    unique_items=True,
    regex=_validate.TAG_REGEX
)
comments = _Field(
    default_factory=list,
    description="Comments on the post",
)

mimetype:str = _Field(
    ...,
    description="The MIME type for the File",
    regex="^[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+$",
)
item_id = _Field(
    ...,
    description="The Unique ID for this Item",
)