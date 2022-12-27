from . import BaseModel, fields
from pydantic import Field


class Subscription(BaseModel):
    created_at: float = fields.created_at
    id: int = Field(..., description="The subscription's ID")
    creator: int|None = Field(..., description="The creator's ID")
    
    url: str = Field(..., description="The url subscribed to")
    last_checked:float = Field(default_factory=0, description="The Unix timestamp for when this was last checked",)
    collected_urls: list[str] = Field(default_factory=None, description="The discovered URLs")


class SubscriptionQuery(BaseModel):
    index: int = Field(default=0, gt=0)
    limit: int = Field(default=100, gt=0, le=100)
    creator: int|None = Field(default=None, description="The Creator's ID")
