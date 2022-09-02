from . import router
from modules import schemas, posts, account, database
from modules.fastapi.dependencies import DecodeToken, RequirePermission, RateLimit, RequireCaptcha
from fastapi import status, UploadFile, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.get("/permissions",
    response_model=schemas.UserPermissions,
)
async def get_permissions(user:account.Account = Depends(DecodeToken)):
    perms = user.permissions.permissions
    return JSONResponse(jsonable_encoder(perms))