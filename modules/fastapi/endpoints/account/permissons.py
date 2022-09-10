from . import router
from modules import schemas, fastapi
from fastapi import Depends
from typing import Union


@router.get("/permissions",
    operation_id="permissions",
    response_model=schemas.UserPermissions,
    dependencies=[
        Depends(fastapi.RateLimit("1/second")),
    ],
)
async def get_permissions(account: fastapi.DecodeToken = Depends()):
    return account.permissions.permissions
