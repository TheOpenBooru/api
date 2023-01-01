from . import router
from openbooru.modules import schemas, database
from openbooru.modules.fastapi.dependencies import PermissionManager
from fastapi import Depends


@router.post("/search",
    response_model=list[schemas.Subscription],
    dependencies=[
        Depends(PermissionManager("canSearchSubscriptions")),
    ],
)
async def search_subscriptions(query: schemas.SubscriptionQuery):
    return database.Subscriptions.search(
        query.index,
        query.limit,
        query.creator
    )