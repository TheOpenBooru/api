from . import router
from openbooru.modules import schemas, fastapi
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/permissions",
    response_model=schemas.UserPermissions,
    dependencies=[
        Depends(fastapi.RateLimit("1/second")),
    ],
)
async def get_permissions(account: fastapi.GetAccount = Depends()):
    perms = account.permissions.schema
    return JSONResponse(content=jsonable_encoder(perms))
