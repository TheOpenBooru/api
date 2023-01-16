from . import router
from modules import schemas, database
from modules.fastapi.dependencies import GetAccount, PermissionManager
from fastapi import Depends, HTTPException


@router.post("/create",
    response_model=schemas.Subscription,
    responses= {
        400:{"description": "Failed To Create Subscription"},
        409:{"description": "Subscription Already Exists"},
    },
    dependencies=[
        Depends(PermissionManager("canCreateSubscriptions")),
    ],
)
async def create_subscription(url: str, account: GetAccount = Depends()):
    subscription = schemas.Subscription(
        id=database.Subscriptions.get_unique_id(),
        creator=account.user_id,
        url=url
    )
    try:
        database.Subscriptions.insert(subscription)
    except KeyError: 
        raise HTTPException(409, "Subscription Already Exists")
    except:
        raise HTTPException(400, "Failed To Create Subscription")
    else:
        return subscription