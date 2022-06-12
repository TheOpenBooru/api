from . import router
from .._token import Account, DecodeToken
from modules import database
from fastapi import Response, Depends, Body, status



@router.put(
    "/settings",
    responses={
        200:{"description":"Profile Data Retrieved Successfully"},
        400:{"description":"Not Logged In"},
    },
)
async def update_settings(
        settings:str = Body(description="Settings to be stored on the user's profile, 4096 characters max"),
        account:Account = Depends(DecodeToken)
        ):
    try:
        database.User.updateSettings(account.id,settings)
        return Response(status_code=200)
    except ValueError:
        
        return Response(status_code=200)
        
