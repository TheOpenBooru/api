from . import router
from modules import database, fastapi, account
from fastapi import Response, Depends, Body, status


@router.put(
    "/settings",
    responses={
        400:{"description":"Settings is larger than 4096 Retrieved Successfully"},
        401:{"description":"Not Logged In"},
    },
)
async def update_settings(
        settings:str = Body(description="Settings to be stored on the user's profile, 4096 characters max"),
        account:account.Account = Depends(fastapi.DecodeToken)
        ):
    if len(settings) > 4096:
        return Response(status_code=400)
    else:
        database.User.updateSettings(account.id,settings)
        return Response(status_code=200)
